FROM python:3.8.6

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo

RUN mkdir /opt/speech_recognition_open_api/
WORKDIR /opt/speech_recognition_open_api/


COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /opt/speech_recognition_open_api
EXPOSE 50051
RUN sh /opt/speech_recognition_open_api/model_bootstrap.sh
CMD ["python","/opt/speech_recognition_open_api/server.py"]
