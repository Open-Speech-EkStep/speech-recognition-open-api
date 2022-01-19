FROM gcr.io/ekstepspeechrecognition/speech-recognition-open-api-dependency:3.1


ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo wget python3-pip

RUN mkdir /opt/speech_recognition_open_api/
ENV base_path=/opt/speech_recognition_open_api/
ENV models_base_path=/opt/speech_recognition_open_api/deployed_models/
ENV model_logs_base_path=/opt/speech_recognition_open_api/deployed_models/logs/
ENV TRANSFORMERS_CACHE=/opt/speech_recognition_open_api/deployed_models/model_data/transformers_cache/
ENV DENOISER_MODEL_PATH=/opt/speech_recognition_open_api/deployed_models/model_data/denoiser/
ENV UTILITIES_FILES_PATH=/opt/files/
COPY requirements.txt /opt/speech_recognition_open_api/
RUN echo "export LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/lib" >> ~/.bashrc
RUN pip3 install --no-cache-dir -r /opt/speech_recognition_open_api/requirements.txt
WORKDIR /opt/speech_recognition_open_api/
COPY . /opt/speech_recognition_open_api
RUN cp -r /opt/files/denoiser /opt/speech_recognition_open_api/denoiser
CMD ["python3","/opt/speech_recognition_open_api/server.py"]

