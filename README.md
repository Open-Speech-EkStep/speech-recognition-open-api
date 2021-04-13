First install required libraries using the following command:
```
pip install -r requirements.txt
```

To generate stub files from .proto file, use the following command:
```
python -m grpc_tools.protoc --proto_path=./proto ./proto/speech-recognition-open-api.proto --python_out=./stub --grpc_python_out=./stub
```

To run tests, use the following command:
```
py.test --grpc-fake-server
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