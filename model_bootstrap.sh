#!/usr/bin/env bash
echo "Setting up model dependencies...."
sudo apt-get install -y liblzma-dev libbz2-dev libzstd-dev libsndfile1-dev libopenblas-dev libfftw3-dev libgflags-dev libgoogle-glog-dev
sudo apt install -y build-essential cmake libboost-system-dev libboost-thread-dev libboost-program-options-dev libboost-test-dev libeigen3-dev zlib1g-dev libbz2-dev liblzma-dev netcat


git clone https://github.com/kpu/kenlm.git
cd kenlm
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DKENLM_MAX_ORDER=20 -DCMAKE_POSITION_INDEPENDENT_CODE=ON
make -j16
cd ../../
export KENLM_ROOT_DIR=$PWD
export USE_CUDA=0 ## for cpu

rm -rf kenlm



git clone https://github.com/facebookresearch/wav2letter.git -b v0.2
cd wav2letter/bindings/python
pip install -e .
cd ../../../
rm -rf wav2letter


git clone https://github.com/Open-Speech-EkStep/wav2vec-infer.git -b staging
cd wav2vec-infer/wav2vec
pip install -e .
cd ../../

rm -rf wav2vec-infer

if [ "$1" = "start_server" ];then
  echo "Starting the grpc server...."
  python /opt/speech_recognition_open_api/server.py
fi
