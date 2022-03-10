import os

import grpc
from stub.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
from main import read_audio, transcribe_url, transcribe_audio_bytes

if __name__ == '__main__':
    host = "34.121.100.224"
    port = 50051
    with grpc.insecure_channel('{}:{}'.format(host, port)) as channel:
        stub = SpeechRecognizerStub(channel)
        language = 'hi'
        audio_url = 'https://storage.googleapis.com/test_public_bucket/download.mp3'

        response = transcribe_url(stub, audio_url, language, 'mp3', 'transcript')
        print(response.output[0].source)

        response = transcribe_url(stub, audio_url, language, 'mp3', 'srt')
        print(response.output[0].source)

        audio_bytes = read_audio('changed.wav')
        response = transcribe_audio_bytes(stub, audio_bytes, language, 'wav', 'transcript')
        print('Response from Audio bytes:'+response.output[0].source)

        response = transcribe_audio_bytes(stub, audio_bytes, language, 'wav', 'srt')
        print('Response from Audio bytes:'+response.output[0].source)
