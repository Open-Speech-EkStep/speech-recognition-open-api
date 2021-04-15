First install required libraries using the following command:
```
pip install -r requirements.txt
```

To generate stub files from .proto file, use the following command:
```
python -m grpc_tools.protoc --proto_path=./proto ./proto/speech-recognition-open-api.proto --python_out=./stub --grpc_python_out=./stub

or


python3 -m grpc_tools.protoc \
    --include_imports \
    --include_source_info \
    --proto_path=./proto \
    ./proto/google/api/http.proto \
    ./proto/google/api/annotations.proto \
    -I ./proto \
    --descriptor_set_out=api_descriptor.pb \
    --python_out=./stub \
    --grpc_python_out=./stub \
    ./proto/speech-recognition-open-api.proto
```

To run tests, use the following command:
```
py.test --grpc-fake-server
```

`DOC: https://cloud.google.com/api-gateway/docs/get-started-cloud-run-grpc#before_you_begin`

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