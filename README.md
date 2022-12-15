# Speech Recogntition Open API

## Getting started guide:

This is a [GRPC](https://grpc.io/) based service which also supports streaming for realtime inferencing. Proto file for grpc is available at [proto/speech-recognition-open-api.proto](proto/speech-recognition-open-api.proto). It has tree endpoints 

| Endpoint        | Purpose                                |
|-----------------|----------------------------------------|
| recognize_audio | Streaming Endpoint.                    |
| punctuate       | Punctuation endpoint for a given text. |
| recognize       | Inferencing from a audio URL or bytes. |

### Setup models

Download asr models and punctuation models. Thereafter, update the right asr model paths in model_dict.json. Docker image expects all the models and config to be available at directory `/opt/speech_recognition_open_api/deployed_models/`.

**Sample `deployed_models` directory structure**

```shell
|-- gujarati
|   |-- dict.ltr.txt
|   `-- gujarati.pt
|-- hindi
|   |-- dict.ltr.txt
|   |-- hindi.pt
|   |-- lexicon.lst
|   `-- lm.binary
|-- hinglish
|   |-- dict.ltr.txt
|   |-- hinglish_CLSRIL.pt
|   |-- lexicon.lst
|   `-- lm.binary
|-- model_dict.json
|-- model_data
|   |-- albert_metadata
|   |   |-- config.json
|   |   |-- pytorch_model.bin
|   |   |-- spiece.model
|   |   `-- spiece.vocab
|   |-- as.json
|   |-- as.pt
|   |-- as_dict.json
|   |-- bn.json
|   |-- bn.pt
|   |-- bn_dict.json
|   |-- denoiser
|   |   `-- denoiser_dns48.pth  #Denoiser checkout details are https://github.com/Open-Speech-EkStep/denoiser
```

**ASR Models**

All the open-source language models are available at bucket https://console.cloud.google.com/storage/browser/vakyansh-open-models/models/. You can find more details about the same at https://github.com/Open-Speech-EkStep/vakyansh-models#language-models-works-with-finetuned-asr-models.

**Punctuation models:**

Punctuation models are stored inside `model_data` directory of `deployed_models` directory and then download all punc models. Details of open sourced punctuation models are available https://github.com/Open-Speech-EkStep/vakyansh-models#punctuation-models.

```
gu/:
wget https://storage.googleapis.com/vakyansh-open-models/punctuation_models/gu/gu.json .
wget https://storage.googleapis.com/vakyansh-open-models/punctuation_models/gu/gu.pt .
wget https://storage.googleapis.com/vakyansh-open-models/punctuation_models/gu/gu_dict.json .

hi/:
wget https://storage.googleapis.com/vakyansh-open-models/punctuation_models/hi/hi.json .
wget https://storage.googleapis.com/vakyansh-open-models/punctuation_models/hi/hi.pt .
wget https://storage.googleapis.com/vakyansh-open-models/punctuation_models/hi/hi_dict.json .
```

Once all the required models are placed `model_dict.json` file should be updated with relative paths to the asr model artifacts.

For eg, if the asr models are placed in the directory /asr-models/,then model_dict.json would be like,
```
{
    "en": {
        "path": "/asr-models/indian_english/final_model.pt",
        "enablePunctuation": true,
        "enableITN": true
    },
    "hi": {
        "path": "/asr-models/hindi/hindi.pt",
        "enablePunctuation": true,
        "enableITN": true
    }
}

```




#### With docker

**Using pre-built docker image:**

We have pre-built images hosted on `gcr.io/ekstepspeechrecognition/speech_recognition_model_api`. You can use these images directly to run on docker. 

Note: We do not follow `latest` tag, so you have to specify exact version.

```shell
docker run -itd -p 50051:50051  --env gpu=True --env languages=['en','hi']  --gpus all -v <Location for deployed_models directory>:/opt/speech_recognition_open_api/deployed_models/ gcr.io/ekstepspeechrecognition/speech_recognition_model_api:3.2.33
```

### Using example to test

We have python and java client [examples](examples) available in this repo which can be used to test.

pyhton secure example can be run from [examples/python/speech-recognition](examples/python/speech-recognition)

```shell
python main.py
```

For insecure example

```shell
python main-insecure.py
```


### Using GRPC clients:

This is a GRPC service you can call it using any GRPC supported client. Complete details of request/response schema can be found in [ULCA Schema](https://github.com/ULCA-IN/ulca/blob/master/specs/model-schema.yml).

Proto file for the GRPC service is available at [proto/speech-recognition-open-api.proto] (proto/speech-recognition-open-api.proto)

**Popular GRPC Clients**

* [BloomRPC](https://github.com/bloomrpc/bloomrpc)
* [Grpcurl](https://github.com/fullstorydev/grpcurl)
* Postman

API supported two transcription formats:
* transcript
* srt

**Sample request for ASR with audio URL**
```json
{
    "config": {
      "language": {
      "sourceLanguage": "hi"
    },
        "transcriptionFormat": {
            "value": "transcript"
        },
        "audioFormat": "wav",
        "punctuation": true,
        "enableInverseTextNormalization": true
    },
    "audio": [
        {
            "audioUri": "https://storage.googleapis.com/test_public_bucket/srt_test.wav"
        }
    ]
}
```

**Sample request for ASR with Audio bytes**
```json
{
    "config": {
      "language": {
      "sourceLanguage": "hi"
    },
        "transcriptionFormat": {
            "value": "transcript"
        },
        "audioFormat": "wav",
        "punctuation": true,
        "enableInverseTextNormalization": true
    },
    "audio": [
        {
            "audioContent": "<Audio Bytes>"
        }
    ]
}
```


**Sample ASR Response**

```json
{
    "status": "SUCCESS",
    "output": [
        {
            "source": "मैं भारत देश का निवासी हूँ"
        }
    ]
}
```

**Sample request in grpcurl**

```shell
grpcurl -import-path <directory to proto file> -proto speech-recognition-open-api.proto -plaintext -d @ localhost:50051 ekstep.speech_recognition.SpeechRecognizer.recognize <<EOM
{
    "config": {
      "language": {
      "sourceLanguage": "hi"
    },
        "transcriptionFormat": {
            "value": "transcript"
        },
        "audioFormat": "wav",
        "punctuation": true,
        "enableInverseTextNormalization": true
    },
    "audio": [
        {
            "audioUri": "https://storage.googleapis.com/test_public_bucket/srt_test.wav"
        }
    ]
}
EOM
```

### Realtime Streaming

Realtime streaming can be supported directly using GRPC. If you need something to work on browser, we have a socket.io based implementation. Refer the [documentation](https://open-speech-ekstep.github.io/asr_streaming_service/)

### Generating stubs form proto

As this is a GRPC service, all the endpoints are defined in proto file. Once you made changes into proto file you need to generate stubs for it.

To generate stub files from .proto file, using the following command:

```shell
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


### To run tests

```shell
py.test --grpc-fake-server --ignore=wav2letter --ignore=wav2vec-infer --ignore=kenlm
```

#### Test Coverage

1. Install coverage library using the following command: `pip3 install pytest-cov`
2. Run the following command to get coverage report: `pytest --cov=src tests/ --grpc-fake-server`

### Building your own docker image

We build this app in two steps to expedite the process of changes in the main source. We build a dependency image for which you can find dependency docker image file at [dependencies/Dockerfile](dependencies/Dockerfile). 

Using dependency image, we build the main images which are published. Docker file for this step is available [here](Dockerfile). You can use these steps to recreate the bundle. We recommend using some environment manager like [conda](https://github.com/conda/conda).


### Running with source code

You can follow the steps from dependency docker image [dependencies/Dockerfile](dependencies/Dockerfile) and main docker image [file](Dockerfile). After setup the directory and installing all the prerequisites, yu can run `server.py` file to start grpc server. Default port of the GRPC server is 50051 which can be changed from [server.py](server.py).

```shell
python server.py
```


### Supported environment variables

| **Variable Name**    | **Default Value**                                                                       | **Description**                                                           |
|----------------------|-----------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| log_level            | DEBUG                                                                                   | Log level for application logs                                            |
| gpu                  | True                                                                                    | True: Load the models on GPU,  False: Use CPU                             |
| model_logs_base_path | /opt/speech_recognition_open_api/deployed_models/logs/                                  | Location for language model folders.                                      |
| TRANSFORMERS_CACHE   | /opt/speech_recognition_open_api/deployed_models/model_data/transformers_cache/         | Transformers cache location for punctuation                               |
| DENOISER_MODEL_PATH  | /opt/speech_recognition_open_api/deployed_models/model_data/denoiser/denoiser_dns48.pth | Denoiser checkpoint. Refer https://github.com/Open-Speech-EkStep/denoiser |
