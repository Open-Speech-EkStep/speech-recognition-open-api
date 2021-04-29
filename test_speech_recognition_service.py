import os

import pytest
from unittest.mock import patch
from stub.speech_recognition_open_api_pb2 import SpeechRecognitionRequest, RecognitionConfig, \
    RecognitionAudio, Language, SpeechRecognitionResult


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from stub.speech_recognition_open_api_pb2_grpc import add_SpeechRecognizerServicer_to_server
    return add_SpeechRecognizerServicer_to_server


@pytest.fixture(scope='module')
@patch('speech_recognition_service.ModelService')
def grpc_servicer(model_mock):
    from speech_recognition_service import SpeechRecognizer
    model_mock.return_value.transcribe.return_value = {'transcription': 'Hello world'}
    return SpeechRecognizer()


@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from stub.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
    return SpeechRecognizerStub


def test_if_audio_url_is_handled(grpc_stub, mocker):
    def download_mock(file_name, audio_uri):
        return '/home/test'

    mocker.patch('os.remove')
    mocker.patch('speech_recognition_service.download_from_url_to_file', download_mock)

    audio_url = "http://localhost/audio.mp3"

    lang = Language(value='en', name='English')
    config = RecognitionConfig(language=lang, transcriptionFormat='TRANSCRIPT', samplingRate='_44KHZ')
    audio = RecognitionAudio(audioUri=audio_url)
    request = SpeechRecognitionRequest(audio=audio, config=config)
    resp = grpc_stub.recognize(request)

    assert SpeechRecognitionResult.Status.Name(resp.status) == 'SUCCESS'
    assert resp.transcript == 'Hello world'
    os.remove.assert_called_once_with('/home/test')


def test_if_audio_bytes_is_handled(grpc_stub, mocker):
    def save_mock(file_name, audio_data):
        return '/home/test'

    mocker.patch('os.remove')
    mocker.patch('speech_recognition_service.create_wav_file_using_bytes', save_mock)
    
    audio_bytes = b"http://localhost/audio.mp3"
    lang = Language(value='en', name='English')
    config = RecognitionConfig(language=lang, transcriptionFormat='TRANSCRIPT', samplingRate='_44KHZ')
    audio = RecognitionAudio(audioContent=audio_bytes)
    request = SpeechRecognitionRequest(audio=audio, config=config)
    resp = grpc_stub.recognize(request)

    assert SpeechRecognitionResult.Status.Name(resp.status) == 'SUCCESS'
    assert resp.transcript == 'Hello world'
    os.remove.assert_called_once_with('/home/test')

