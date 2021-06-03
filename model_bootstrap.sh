#!/usr/bin/env bash

echo "Setting up model dependencies...."
sudo apt-get update
sudo apt-get install -y liblzma-dev libbz2-dev libzstd-dev libsndfile1-dev libopenblas-dev libfftw3-dev libgflags-dev libgoogle-glog-dev
sudo apt install -y build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev
sudo apt-get install -y ffmpeg

pip3 install git+https://github.com/Open-Speech-EkStep/indic-punct.git#egg=indic-punct
pip3 install ray[tune]

if [ ! -d kenlm ]; then
  git clone https://github.com/kpu/kenlm.git
fi
cd kenlm
mkdir -p build && cd build
cmake ..
make -j 16
cd ..
export KENLM_ROOT_DIR=$PWD
export USE_CUDA=0 ## for cpu
cd ..

# rm -rf kenlm


if [ ! -d wav2letter ]; then
  git clone -b v0.2 https://github.com/facebookresearch/wav2letter.git
fi
cd wav2letter
cd bindings/python
pip3 install -e .
cd ../../../
# rm -rf wav2letter

if [ ! -d wav2vec-infer ]; then
  git clone https://github.com/Open-Speech-EkStep/wav2vec-infer.git -b modularization
fi
cd wav2vec-infer/wav2vec
pip3 install -e .
cd ../../


if [ ! -d denoiser ]; then
  git clone https://github.com/facebookresearch/denoiser.git
fi



