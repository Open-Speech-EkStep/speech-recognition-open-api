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
4. Download asr models and punc models.Thereafter, update the right asr model paths in model_dict.json.
**Asr models:**
Create deployed_models directory and download the models inside it.

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

**Language Models**

All the opensourced language models are available at https://console.cloud.google.com/storage/browser/vakyansh-open-models/models/. Find all the details in https://github.com/Open-Speech-EkStep/vakyansh-models#language-models-works-with-finetuned-asr-models.

**Punctuation models:**

Create a directory called `model_data` inside deployed_models directory and then download all punc models. Open sourced punctuation models are available https://github.com/Open-Speech-EkStep/vakyansh-models#punctuation-models.

```
gu/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/gu/gu.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/gu/gu.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/gu/gu_dict.json .

hi/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi_dict.json .
```
model_dict(same hierarchy as deployed_models directory) file should be updated with relative paths to the asr model artifacts:
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



5. Start the server at port 50051:

```shell
python server.py
```
#### With docker


**Build Docker image:**

```shell
docker build -t speech_recognition_model_api .
```

**Build Docker image:**

```shell
docker run -itd -p <<host_port>>:50051 --name speech_recognition_model_api -v <<host_model_path>>/deployed_models:<<container_model_path>>/deployed_models/ -i -t speech_recognition_model_api
```

**Using pre-built docker image:**

We have pre-built images hosted on `gcr.io/ekstepspeechrecognition/speech_recognition_model_api`. You can use these images directly to run on docker. 

Note: We do not follow `latest` tag, so you have to specify exact version.

```shell
docker run -itd -p 50051:50051  --env gpu=True --env languages=['en','hi']  --gpus all -v <Location for deployed_models directory>:/opt/speech_recognition_open_api/deployed_models/ gcr.io/ekstepspeechrecognition/speech_recognition_model_api:3.2.33
```

### Using example to test:

We have python and java client [examples](examples) available in this repo which can be used to test.

Pyhton example can be run as
```shell
python examples/python/speech-recognition/main.py
```

### Using GRPC clients:

This is a GRPC service you can call it using any GRPC supported client. Complete details of request/response schema can be found in [ULCA Schema](https://github.com/ULCA-IN/ulca/blob/master/specs/model-schema.yml).

**Sample request with Audio URL**
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

**Sample request with Audio bytes**
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


**Sample Response**

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

### Developer Guide

The api, protobuf are taken from google folder from the below repo: `https://github.com/googleapis/googleapis`

Generated stub files from .proto file, using the following command:

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


To run tests, use the following command:

```shell
py.test --grpc-fake-server --ignore=wav2letter --ignore=wav2vec-infer --ignore=kenlm
```

`DOC: https://cloud.google.com/api-gateway/docs/get-started-cloud-run-grpc#before_you_begin`
