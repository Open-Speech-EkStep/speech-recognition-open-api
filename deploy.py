import yaml
import argparse
from collections import OrderedDict
import os
import subprocess

def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def ordered_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

def cmd_runner(command, caller):
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.stderr:
        raise subprocess.CalledProcessError(
                returncode = result.returncode,
                cmd = result.args,
                stderr = result.stderr
                )
    if result.stdout:
        print("Helm deployment => ", caller, " Out => ", result.stdout.decode('utf-8'), "\n")


class LanguageConfig:

    def __init__(self, language_code, base_name, helm_chart_path):
        self.language_code = language_code
        self.helm_chart_path = helm_chart_path
        self.release_name = "{}-{}".format(base_name, language_code)
    
    def is_deployed(self, namespace):
        result = subprocess.getoutput('helm status {} -n {} --output yaml'.format(self.release_name, namespace))
        if result == "Error: release: not found":
            return False
        else:
            return True

    def deploy(self, namespace, api_changed):
        if api_changed or not self.is_deployed(namespace):
            process = "install"
        else:
            process = "upgrade"
        command = "helm {0} --timeout 180s {1} {2} --namespace {3} --set env.languages='[\"{4}\"]'".format(process, self.release_name, self.helm_chart_path, namespace, self.language_code)
        if api_changed:
            uninstall_command = "helm uninstall {0} --namespace {1}".format(self.release_name, namespace)
            cmd_runner(uninstall_command, "LANGUAGE :" + self.language_code)
            cmd_runner(command, "LANGUAGE :" + self.language_code)
        else:    
            cmd_runner(command, "LANGUAGE :" + self.language_code)

class EnvoyConfig:

    def __init__(self, base_name, crt, key, helm_chart_path):
        self.name = "envoy"
        self.crt = crt
        self.key = key
        self.helm_chart_path = helm_chart_path
        self.release_name = "{}-{}".format(base_name, self.name)
    
    def is_deployed(self, namespace):
        result = subprocess.getoutput('helm status {} -n {} --output yaml'.format(self.release_name, namespace))
        if result == "Error: release: not found":
            return False
        else:
            return True

    def deploy(self, namespace):
        if not self.is_deployed(namespace):
            process = "install"
        else:
            process = "upgrade"
        command = "helm {0} --timeout 180s {1} {2} --namespace {3} --set creds.crt={4} --set creds.key={5}".format(process, self.release_name, self.helm_chart_path, namespace, self.crt, self.key)
        cmd_runner(command, "Envoy")

def read_app_config(config_path):
    with open(config_path, "r") as stream:
        try:
            config = ordered_load(stream, yaml.SafeLoader)
            return config
        except yaml.YAMLError as exc:
            print("Error: ", exc)
            return None

def read_envoy_config(config_path):
    with open(config_path, "r") as stream:
        try:
            config = ordered_load(stream, yaml.SafeLoader)
            return config
        except yaml.YAMLError as exc:
            print("Error: ", exc)
            return None

def get_cluster(clusters, language_code):
    cluster_name = "{}_cluster".format(language_code)
    for cluster in clusters:
        if cluster["name"] == cluster_name:
            return cluster
    return None

def clear_clusters_and_matches(language_code):
    pass

def create_cluster(language_config):
    cluster = '''
        name: hi_cluster
        type: LOGICAL_DNS
        lb_policy: ROUND_ROBIN
        connect_timeout: 30s
        dns_lookup_family: V4_ONLY
        typed_extension_protocol_options:
          envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
            "@type": type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions
            explicit_http_config:
              http2_protocol_options: {}
        load_assignment:
          cluster_name: hi_cluster
          endpoints:
          - lb_endpoints:
            - endpoint:
                address:
                  socket_address:
                    address: asr-model-v2-hi
                    port_value: 50051
    '''
    cluster = ordered_load(cluster, yaml.SafeLoader)
    cluster_name = "{}_cluster".format(language_config.language_code)
    cluster["name"] = cluster_name
    cluster["load_assignment"]["cluster_name"] = cluster_name
    cluster["load_assignment"]["endpoints"][0]["lb_endpoints"][0]["endpoint"]["address"]["socket_address"]["address"] = language_config.release_name
    return cluster

def verify_and_update_release_name(cluster, release_name):
    address = cluster["load_assignment"]["endpoints"][0]["lb_endpoints"][0]["endpoint"]["address"]["socket_address"]["address"]
    if address != release_name:
        cluster["load_assignment"]["endpoints"][0]["lb_endpoints"][0]["endpoint"]["address"]["socket_address"]["address"] = release_name

def update_envoy_config(config, language_config):
    listeners = config["static_resources"]["listeners"]
    clusters = config["static_resources"]["clusters"]
    routes = listeners[0]["filter_chains"][0]["filters"][0]["typed_config"]["route_config"]["virtual_hosts"][0]["routes"]

    # updating cluster information
    cluster = get_cluster(clusters, language_config.language_code)
    if cluster is None:
        lang_cluster = create_cluster(language_config)
        clusters.append(lang_cluster)
        cluster = lang_cluster
    else:
        verify_and_update_release_name(cluster, language_config.release_name)
    # updating match filter
    grpc_match_route = get_grpc_match_filter(routes, language_config.language_code)
    if grpc_match_route is None:
        grpc_match_route = create_grpc_match_filter(language_config, cluster["name"])
        routes.insert(len(routes)-2, grpc_match_route)

    rest_match_route = get_rest_match_filter(routes, language_config.language_code)
    if rest_match_route is None:
        rest_match_route = create_rest_match_filter(language_config, cluster["name"])
        routes.insert(len(routes)-2, rest_match_route)
    
    return config

def write_to_yaml(config, path):
    with open(path, "w") as file:
        try:
            ordered_dump(config, stream= file, Dumper=yaml.SafeDumper)
        except yaml.YAMLError as exc:
            print("Error: ", exc)

def create_grpc_match_filter(language_config, cluster_name):
    route_match = '''
        match:
          prefix: "/ekstep.speech_recognition.SpeechRecognizer/recognize"
          headers:
          - name: language
            exact_match: "hi"
        route: {cluster: hi_cluster, timeout: 60s}
    ''' 
    route_match = ordered_load(route_match, yaml.SafeLoader)
    route_match["match"]["headers"][0]["exact_match"] = language_config.language_code
    route_match["route"]["cluster"] = cluster_name
    return route_match

def create_rest_match_filter(language_config, cluster_name):
    route_match = '''
        match:
          prefix: "/v1/recognize/hi"
        route: {cluster: hi_cluster, timeout: 60s}
    '''
    route_match = ordered_load(route_match, yaml.SafeLoader)
    route_match["match"]["prefix"] = "/v1/recognize/{}".format(language_config.language_code)
    route_match["route"]["cluster"] = cluster_name
    return route_match

def get_grpc_match_filter(routes, language_code):
    path_to_match = "/ekstep.speech_recognition.SpeechRecognizer/recognize"
    for route in routes:
        if route["match"]["prefix"] == path_to_match:
            if "headers" in route["match"] and route["match"]["headers"][0]["exact_match"] == language_code:
                return route
    return None

def get_rest_match_filter(routes, language_code):
    path_to_match = "/v1/recognize/{}".format(language_code)
    for route in routes:
        if route["match"]["prefix"] == path_to_match:
            return route
    return None

def update_proto_descriptor(config, path_to_pb_file):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--namespace', default='test-v2', help="Namespace to use")
    # parser.add_argument('--app-config-path', help="Path of the app config")
    # parser.add_argument('--envoy-config-path', help="envoy config path")
    parser.add_argument('--crt', help="Crt for certificate", required = True)
    parser.add_argument('--key', help="key for certificate", required = True)
    parser.add_argument('--api-updated', default= False, help="Flag if api has changed", required = True)

    args = parser.parse_args()

    namespace = args.namespace
    api_updated = args.api_updated
    app_config_path = "app_config.yaml"
    envoy_config_path = "infra/envoy/config.yaml"
    language_helm_chart_path = "infra/asr-model-v2"
    envoy_helm_chart_path = "infra/envoy"
    envoy_config = read_envoy_config(envoy_config_path)
    app_config = read_app_config(app_config_path)
    if envoy_config is None:
        print("Check the envoy config file")
        exit()
    if app_config is None:
        print("Check the app config file")
        exit()

    release_name = app_config["base_name"]
    languages = app_config["languages"]
    for language_code in languages:
        language_config = LanguageConfig(language_code, release_name, language_helm_chart_path)
        language_config.deploy(namespace, api_updated)
        envoy_config = update_envoy_config(envoy_config, language_config)

    # clear_clusters_and_matches(languages)

    write_to_yaml(envoy_config, envoy_config_path)
    EnvoyConfig(release_name, args.crt, args.key, envoy_helm_chart_path).deploy(namespace)
