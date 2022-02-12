FROM nvidia/cuda:11.6.0-devel-ubuntu20.04


ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /opt/api_dependencies/

COPY installer.sh /opt/api_dependencies/
RUN sh /opt/api_dependencies/installer.sh
WORKDIR /opt/api_dependencies/
