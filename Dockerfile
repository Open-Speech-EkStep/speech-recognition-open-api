FROM python:3.8.6

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo
#RUN apt-get install -y wget
#RUN apt-get install -y curl
#RUN apk add --update --no-cache \
#    gcc \
#    linux-headers \
#    make \
#    musl-dev \
#    python3-dev \
#    g++

RUN mkdir /opt/speech_recognition_open_api/
WORKDIR /opt/speech_recognition_open_api/


COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /opt/speech_recognition_open_api
RUN sudo chown 777 /opt/speech_recognition_open_api/model_bootstrap.sh
EXPOSE 50051
CMD ["sh","/opt/speech_recognition_open_api/model_bootstrap.sh"]
CMD ["python","/opt/speech_recognition_open_api/server.py"]
