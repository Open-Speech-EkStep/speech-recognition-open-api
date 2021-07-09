FROM continuumio/miniconda3
#RUN conda create -n fairseq python=3.8
#RUN echo "conda activate fairseq" > ~/.bashrc
#ENV PATH /opt/conda/envs/fairseq/bin:$PATH
#RUN . ~/.bashrc

#ENV PATH="/opt/miniconda3/bin:${PATH}"
#ARG PATH="/opt/miniconda3/bin:${PATH}"
#RUN conda --version
#RUN conda info
#RUN conda activate fairseq

#RUN conda --version
#RUN pip3 --version
#RUN conda info
#RUN wget \
#    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#    && mkdir /opt/.conda \
#    && bash Miniconda3-latest-Linux-x86_64.sh -b \
#    && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN mkdir /opt/speech_recognition_open_api/
WORKDIR /opt/speech_recognition_open_api/
COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run","--no-capture-output","-n", "fairseq", "/bin/bash", "-c"]
RUN conda info
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sudo wget python3-pip
COPY requirements.txt .
#RUN pip3 install --upgrade pip3
#RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /opt/speech_recognition_open_api
EXPOSE 50051
RUN sh /opt/speech_recognition_open_api/model_bootstrap.sh
CMD ["conda", "run", "--no-capture-output", "-n", "fairseq","python","/opt/speech_recognition_open_api/server.py"]
