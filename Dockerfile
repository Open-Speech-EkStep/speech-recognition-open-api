FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04


ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get install -y sudo wget python3-pip
RUN mkdir /opt/speech_recognition_open_api/
WORKDIR /opt/speech_recognition_open_api/
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /opt/speech_recognition_open_api
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo wget python3-pip
RUN sh /opt/speech_recognition_open_api/model_bootstrap.sh
RUN apt install -y graphviz
RUN wget http://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.8.1.tar.gz
RUN tar -xzf openfst-1.8.1.tar.gz
WORKDIR /opt/speech_recognition_open_api/openfst-1.8.1/
RUN apt install -y gcc-10 gcc-10-base gcc-10-doc g++-10 libstdc++-10-dev libstdc++-10-doc
RUN sh ./configure --enable-grm --enable-far=true && sudo make -j install
RUN echo "export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib" >> ~/.bashrc
RUN sh ~/.bashrc
WORKDIR /opt/speech_recognition_open_api/
RUN wget http://www.openfst.org/twiki/pub/GRM/PyniniDownload/pynini-2.1.4.tar.gz
RUN tar -xzf pynini-2.1.4.tar.gz
WORKDIR /opt/speech_recognition_open_api/pynini-2.1.4/
RUN python3 setup.py install
WORKDIR /opt/speech_recognition_open_api/
RUN apt install python-is-python3

CMD ["python3","/opt/speech_recognition_open_api/server.py"]

