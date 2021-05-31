# Speech Recogntition Open API

## Getting started guide:

### Setup the grpc server:
#### Without docker
1. Create and activate a new enviroment :

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
