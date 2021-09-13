FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu20.04


ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /opt/api_dependencies/
WORKDIR /opt/api_dependencies/
COPY installer.sh .

RUN sh /opt/api_dependencies/installer.sh