FROM gcr.io/ekstepspeechrecognition/speech-recognition-open-api-dependency:1.4


ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo wget python3-pip

RUN mkdir /opt/speech_recognition_open_api/
ENV base_path=/opt/speech_recognition_open_api/
ENV models_base_path=/opt/speech_recognition_open_api/deployed_models/
ENV model_logs_base_path=/opt/speech_recognition_open_api/deployed_models/logs/
WORKDIR /opt/speech_recognition_open_api/
COPY requirements.txt .
RUN echo "export LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/lib" >> ~/.bashrc
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /opt/speech_recognition_open_api
RUN cp -r /opt/files/denoiser /opt/speech_recognition_open_api/denoiser
CMD ["python3","/opt/speech_recognition_open_api/server.py"]

