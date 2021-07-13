#!/usr/bin/env bash
#
echo "Setting up model dependencies...."

apt-get update
apt-get install -y liblzma-dev libbz2-dev libzstd-dev libsndfile1-dev libopenblas-dev libfftw3-dev libgflags-dev libgoogle-glog-dev libfst-tools
apt-get install -y ffmpeg git
apt-get install -y build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev sox

pip3 install packaging soundfile

sudo mkdir -p /opt/files
sudo chmod 777 -R /opt/files
cd /opt/files

if [ ! -d kenlm ]; then
  git clone https://github.com/kpu/kenlm.git
fi
cd kenlm
mkdir -p build && cd build
cmake ..
make -j 16
cd ..
export KENLM_ROOT=$PWD
export USE_CUDA=0 ## for cpu
cd ..


git clone https://github.com/flashlight/flashlight.git
cd flashlight/bindings/python
export USE_MKL=0
python3 setup.py install
pip3 install git+https://github.com/Open-Speech-EkStep/indic-punct.git#egg=indic-punct
conda install -c conda-forge pynini==2.1.4 -y
conda install libgcc gmp

cd /opt/files
if [ ! -d fairseq ]; then
  git clone https://github.com/Open-Speech-EkStep/fairseq -b v2-hydra
fi
cd fairseq
pip3 install -e .
cd ..

pip3 install ray[tune]
pip3 install 'ray[default]'
pip3 install Cython
pip3 install nemo_toolkit[all]==v1.0.2
cd /opt/speech_recognition_open_api/
if [ ! -d denoiser ]; then
  git clone https://github.com/facebookresearch/denoiser.git
fi

