from path_setter import set_root_folder_path
set_root_folder_path()
import os

import pytest
import unittest.mock as mock
from unittest.mock import patch
from stub.speech_recognition_open_api_pb2 import SpeechRecognitionRequest, RecognitionConfig, \
    RecognitionAudio, Language, SpeechRecognitionResult


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from stub.speech_recognition_open_api_pb2_grpc import add_SpeechRecognizerServicer_to_server
    return add_SpeechRecognizerServicer_to_server


@pytest.fixture(scope='module')
@patch('src.speech_recognition_service.ModelService')
def grpc_servicer(model_mock):
    from src.speech_recognition_service import SpeechRecognizer
    model_mock.return_value.transcribe.return_value = {'transcription': 'Hello world', 'status': 'SUCCESS'}
    model_mock.return_value.get_srt.return_value = {'srt': '1\n00:00:01,29 --> 00:00:04,88\nHello how are you\n\n'}
    model_mock.return_value.supported_languages = ['en']
    return SpeechRecognizer()


@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from stub.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
    return SpeechRecognizerStub


def test_if_audio_url_is_handled(grpc_stub, mocker):
    def download_mock(file_name, audio_uri, audio_format):
        return '/home/test'

    mocker.patch('os.remove')
    mocker.patch('src.speech_recognition_service.download_from_url_to_file', download_mock)
    Context = mock.MagicMock()
    mocker.patch('pytest_grpc.plugin.FakeContext', Context)

    audio_url = "http://localhost/audio.mp3"

    lang = Language(sourceLanguage='en', name='English')
    config = RecognitionConfig(language=lang, transcriptionFormat={'value':'srt'}, samplingRate=44000)
    audio = RecognitionAudio(audioUri=audio_url)
    request = SpeechRecognitionRequest(audio=[audio], config=config)

    resp = grpc_stub.recognize(request)

    assert SpeechRecognitionResult.Status.Name(resp.status) == 'SUCCESS'
    assert resp.output[0].source == '1\n00:00:01,29 --> 00:00:04,88\nHello how are you\n\n'


def test_if_audio_bytes_is_handled(grpc_stub, mocker):
    def save_mock(file_name, audio_data):
        return '/home/test'

    mocker.patch('os.remove')
    mocker.patch('src.speech_recognition_service.create_wav_file_using_bytes', save_mock)
    Context = mock.MagicMock()
    mocker.patch('pytest_grpc.plugin.FakeContext', Context)

    audio_bytes = b"http://localhost/audio.mp3"
    lang = Language(sourceLanguage='en', name='English')
    config = RecognitionConfig(language=lang, transcriptionFormat={'value':'transcript'}, samplingRate=44000)
    audio = RecognitionAudio(audioContent=audio_bytes)
    request = SpeechRecognitionRequest(audio=[audio], config=config)
    resp = grpc_stub.recognize(request)

    assert SpeechRecognitionResult.Status.Name(resp.status) == 'SUCCESS'
    assert resp.output[0].source == 'Hello world'


def test_if_given_language_not_implemented(grpc_stub, mocker):
    def handle_request(request, supported_languages):
        raise NotImplementedError('Language not implemented yet')

    mocker.patch('src.speech_recognition_service.handle_request', handle_request)
    Context = mock.MagicMock()
    mocker.patch('pytest_grpc.plugin.FakeContext', Context)
    request = SpeechRecognitionRequest()
    resp = grpc_stub.recognize(request)
    assert SpeechRecognitionResult.Status.Name(resp.status) == 'ERROR'


def test_if_given_out_format_not_implemented(grpc_stub, mocker):
    def handle_request(request, supported_languages):
        raise NotImplementedError('Transcription Format not implemented yet')

    mocker.patch('src.speech_recognition_service.handle_request', handle_request)
    Context = mock.MagicMock()
    mocker.patch('pytest_grpc.plugin.FakeContext', Context)
    request = SpeechRecognitionRequest()

    resp = grpc_stub.recognize(request)
    assert SpeechRecognitionResult.Status.Name(resp.status) == 'ERROR'
