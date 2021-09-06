# Speech Recogntition Open API

## Getting started guide:

### Setup the grpc server:
#### Without docker
1. Create and activate a new environment :

    ```conda create --name <env> python=3.8 && conda activate <env>```

2. Install required libraries using the following command:

    ```
    pip install -r requirements.txt
    ```

3. Bootstrap the model code and other models as pre requisites:

    ```
    sh model_bootstrap.sh
    ```
4. Download models and update the right model paths in model_dict.json.
5. Start the server at port 50051:

    ```
    python server.py
    ```
#### With docker

```
docker build -t speech_recognition_model_api .
```

```
sudo docker run --cpus=6 -m 20000m -itd -p <<host_port>>:50051 --name speech_recognition_model_api -v <<host_model_path>>/deployed_models:<<container_model_path>>/deployed_models/ -i -t speech_recognition_model_api
```

### Using the model api as part of client code:
In python,
```
python examples/python/speech-recognition/main.py
```

### Using the model api as part of REST call using api-gateway:

#### Create api config in api gateway:
```
gcloud api-gateway api-configs create CONFIG_ID \
--api=API_ID --project=PROJECT_ID \
--grpc-files=api_descriptor.pb,api_config.yaml
```

#### Deploy gateway in api gateway:
```
gcloud api-gateway gateways create GATEWAY_ID \
  --api=API_ID --api-config=CONFIG_ID \
  --location=GCP_REGION --project=PROJECT_ID
```
### View gateway information:
```
gcloud api-gateway gateways describe GATEWAY_ID \
  --location=GCP_REGION --project=PROJECT_ID
```

### Test the REST api using a POST request:
```
{
    "config":{
        "language": {
            "value":"hi"
        },
        "transcriptionFormat": "TRANSCRIPT",
        "audioFormat": "WAV"
    },
    "audio":{
        "audioUri": "https://codmento.com/ekstep/test/changed.wav"
    }
}
```

### Developer Guide

The api, protobuf are taken from google folder from the below repo:
```
https://github.com/googleapis/googleapis
```

Generated stub files from .proto file, using the following command:
```
python3 -m grpc_tools.protoc \
    --include_imports \
    --include_source_info \
    --proto_path=./proto \
    ./proto/google/api/http.proto \
    ./proto/google/api/annotations.proto \
    ./proto/google/protobuf/descriptor.proto \
    -I ./proto \
    --descriptor_set_out=./proto/api_descriptor.pb \
    --python_out=./stub \
    --grpc_python_out=./stub \
    ./proto/speech-recognition-open-api.proto
```


To run tests, use the following command:
```
py.test --grpc-fake-server --ignore=wav2letter --ignore=wav2vec-infer --ignore=kenlm
```

`DOC: https://cloud.google.com/api-gateway/docs/get-started-cloud-run-grpc#before_you_begin`


#### Using helm to deploy
#### Prerequisites:
1. Install the following:
```
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo add slamdev-helm-charts https://slamdev.github.io/helm-charts
    helm repo update

    helm install ingress-nginx ingress-nginx/ingress-nginx -n <namespace-name>
    helm install -f envoy-values.yaml asr-model-v2-envoy slamdev-helm-charts/envoy -n <namespace-name>
```
or 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/cloud/deploy.yaml
```

#### Next steps:
1. Do changes if needed in asr-model-v2
2. Run the following to package: `helm package asr-model-v2/`
3. Run the following to install: `helm install <release-name> asr-model-v2-0.1.0.tgz`

To Upgrade:
1. Do changes and package it(Follow steps 1 and 2 in above steps).
2. Run the following to install: `helm upgrade <release-name> asr-model-v2-0.1.0.tgz`

To View all resources:
1. kubectl get all --namespace <namespace-name>
2. `helm list` - to check releases.


Sample grpcurl command:

```

grpcurl -cacert=./../nginx/vakyansh-secret/vakyansh.crt -proto tst.proto -d "{"config": { "language": { "value": "hi" }, "transcriptionFormat": "TRANSCRIPT", "audioFormat": "WAV" }, "audio": { "audioUri": "https://www2.engr.arizona.edu/~429rns/audiofiles/cutafew.wav" } }" model-api.vakyansh.in:443 ekstep.speech_recognition.SpeechRecognizer/recognize

```

#### Note:
In case you get a error such as, ModuleNotFoundError: No module named 'speech_recognition_open_api_pb2',
do the following:

```
Go to stub/speech_recognition_open_api_pb2_grpc.py file, and in the import section change 

'import speech_recognition_open_api_pb2 as speech__recognition__open__api__pb2'
to 
'import stub.speech_recognition_open_api_pb2 as speech__recognition__open__api__pb2'

```

Issue:

1. AttributeError: Can't get attribute 'Wav2VecCtc' on <module '__main__' from 'server.py'>
    Solution: Import Wav2VecCtc in file you are starting.

2. If nginx-ingress is installed and removed later,make sure the ValidatingWebhookConfiguration is removed or it will throw the following error.
```
Error from server (InternalError): error when creating "ingress.yaml": Internal error occurred: failed calling webhook "validate.nginx.ingress.kubernetes.io": Post "https://ingress-nginx-controller-admission.ingress-nginx.svc:443/networking/v1/ingresses?timeout=30s": service "ingress-nginx-controller-admission" not found
```
To resolve it , run the following:
```
kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
kubectl delete -A IngressClass nginx
```