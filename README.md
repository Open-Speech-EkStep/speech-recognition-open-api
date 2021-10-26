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
For asr models:
Create deployed_models directory and download the models inside it.
```js
assamese/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/assamese/assamese.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/assamese/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/assamese/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/assamese/lm.binary .

bengali/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bengali/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bengali/final_model.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bengali/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bengali/lm.binary .

bhojpuri/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bhojpuri/bhojpuri.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bhojpuri/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bhojpuri/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/bhojpuri/lm.binary .

dogri/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/dogri/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/dogri/dogri.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/dogri/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/dogri/lm.binary .

gujarati/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/gujarati/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/gujarati/gujarati.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/gujarati/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/gujarati/lm.binary .

hindi/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/hindi/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/hindi/hindi.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/hindi/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/hindi/lm.binary .

indian_english/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/indian_english/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/indian_english/final_model.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/indian_english/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/indian_english/lm.binary .

kannada/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/kannada/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/kannada/final_model.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/kannada/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/kannada/lm.binary .

maithili/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/maithili/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/maithili/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/maithili/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/maithili/maithili.pt .

malayalam/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/malayalam/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/malayalam/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/malayalam/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/malayalam/malayalam.pt .

marathi/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/marathi/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/marathi/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/marathi/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/marathi/marathi.pt .

nepali/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/nepali/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/nepali/final_model.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/nepali/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/nepali/lm.binary .

odia/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/odia/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/odia/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/odia/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/odia/odia.pt .

punjabi/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/punjabi/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/punjabi/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/punjabi/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/punjabi/punjabi.pt .

rajasthani/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/rajasthani/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/rajasthani/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/rajasthani/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/rajasthani/rajasthani.pt .

sanskrit/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/sanskrit/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/sanskrit/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/sanskrit/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/sanskrit/sanskrit.pt .

tamil/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/tamil/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/tamil/final_model.pt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/tamil/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/tamil/lm.binary .

telugu/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/telugu/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/telugu/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/telugu/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/telugu/telugu.pt .

urdu/:
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/urdu/dict.ltr.txt .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/urdu/lexicon.lst .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/urdu/lm.binary .
wget https://storage.googleapis.com/asr-public-models/data-sources-deployment/urdu/urdu.pt .
```
For punc models:
Create a directory called model_data inside deployed_models directory and then dowload all punc models.
```
gu/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/gu/gu.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/gu/gu.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/gu/gu_dict.json .

hi/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/hi/hi_dict.json .

kn/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/kn/kn.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/kn/kn.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/kn/kn_dict.json .

mr/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/mr/mr.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/mr/mr.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/mr/mr_dict.json .

pa/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/pa/pa.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/pa/pa.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/pa/pa_dict.json .

te/:
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/te/te.json .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/te/te.pt .
wget https://storage.googleapis.com/vakyaansh-open-models/punctuation_models/te/te_dict.json .
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
    },
    "ta": {
        "path": "/asr-models/tamil/final_model.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "bn": {
        "path": "/asr-models/bengali/final_model.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "ne": {
        "path": "/asr-models/nepali/final_model.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "kn": {
        "path": "/asr-models/kannada/final_model.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "gu": {
        "path": "/asr-models/gujarati/gujarati.pt",
        "enablePunctuation": true,
        "enableITN": true
    },
    "te": {
        "path": "/asr-models/telugu/telugu.pt",
        "enablePunctuation": true,
        "enableITN": true
    },
    "or": {
        "path": "/asr-models/odia/odia.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "mr": {
        "path": "/asr-models/marathi/marathi.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "sa": {
        "path": "/asr-models/sanskrit/sanskrit.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "mai": {
        "path": "/asr-models/maithili/maithili.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "bo": {
        "path": "/asr-models/bhojpuri/bhojpuri.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "ml": {
        "path": "/asr-models/malayalam/malayalam.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "raj": {
        "path": "/asr-models/rajasthani/rajasthani.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "doi": {
        "path": "/asr-models/dogri/dogri.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "pa": {
        "path": "/asr-models/punjabi/punjabi.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "ur":{
        "path":"/asr-models/urdu/urdu.pt",
        "enablePunctuation": false,
        "enableITN": false
    },
    "as":{
        "path":"/asr-models/assamese/assamese.pt",
        "enablePunctuation": false,
        "enableITN": false
    }
}

```


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


### Using helm to deploy
#### Prerequisites:
1. To go to infra root folder, run the following: `cd infra`
2. Install the following:
```
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update

    helm install ingress-nginx ingress-nginx/ingress-nginx -n <namespace-name>
```
or 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.0/deploy/static/provider/cloud/deploy.yaml
```
3. To create secret for tls, do the following:
```
kubectl create secret tls asr-model-v2-secret \     
  --cert=vakyansh-secret/vakyansh.crt \
  --key=vakyansh-secret/vakyansh.key -n test
```
#### Next steps:
- To deploy models, do the following:
    1. Do changes if needed in asr-model-v2
    2. Run the following to package: `helm package asr-model-v2/`
    3. Run the following to install: `helm install <release-name> asr-model-v2-<version>.tgz --set namespace=<namespace> --set env.languages='["<language>"]' -n <namespace>`

    To Upgrade:
    1. Do changes and package it(Follow steps 1 and 2 in above steps).
    2. Run the following to install: `helm upgrade <release-name> asr-model-v2-<version>.tgz --set namespace=<namespace> --set env.languages='["<language>"]' -n <namespace>`
- To deploy envoy infra with ingress, do the following:
1. Do changes if needed in asr-model-v2
    2. Run the following to package: `helm package envoy/`
    3. Run the following to install: `helm install <release-name> envoy-<version>.tgz -n <namespace>`

    To Upgrade:
    1. Do changes and package it(Follow steps 1 and 2 in above steps).
    2. Run the following to install: `helm upgrade <release-name> envoy-<version>.tgz -n <namespace>`
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
