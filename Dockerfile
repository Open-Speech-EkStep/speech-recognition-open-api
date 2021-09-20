FROM gcr.io/ekstepspeechrecognition/speech-recognition-open-api-dependency:1.0


ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo wget python3-pip

RUN mkdir /opt/speech_recognition_open_api/
ENV models_base_path=/opt/speech_recognition_open_api/deployed_models/
WORKDIR /opt/speech_recognition_open_api/
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /opt/speech_recognition_open_api
RUN cp -r /opt/files/denoiser /opt/speech_recognition_open_api/denoiser
CMD ["python3","/opt/speech_recognition_open_api/server.py"]

