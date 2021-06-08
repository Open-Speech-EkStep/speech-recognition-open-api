FROM continuumio/miniconda3
RUN conda create -n env python=3.8
RUN echo "source activate fairseq" > ~/.bashrc
ENV PATH /opt/conda/envs/fairseq/bin:$PATH

#ENV PATH="/opt/miniconda3/bin:${PATH}"
#ARG PATH="/opt/miniconda3/bin:${PATH}"
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo wget python3-pip
RUN conda --version
#RUN wget \
#    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#    && mkdir /opt/.conda \
#    && bash Miniconda3-latest-Linux-x86_64.sh -b \
#    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN mkdir /opt/speech_recognition_open_api/
WORKDIR /opt/speech_recognition_open_api/



COPY requirements.txt .
#RUN pip3 install --upgrade pip3
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /opt/speech_recognition_open_api
EXPOSE 50051
RUN sh /opt/speech_recognition_open_api/model_bootstrap.sh
CMD ["python","/opt/speech_recognition_open_api/server.py"]
