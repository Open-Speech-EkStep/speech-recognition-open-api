import pytest

from speech_recognition_service_handler import is_out_format_supported, is_language_supported, handle_request
from stub.speech_recognition_open_api_pb2 import RecognitionConfig, Language, SpeechRecognitionRequest


def test_should_support_given_languages():
    assert is_language_supported('en')
    assert is_language_supported('en-IN')
    assert is_language_supported('hi')
    assert is_language_supported('ta')
    assert is_language_supported('te')
    assert is_language_supported('gu')
    assert is_language_supported('or')
    assert is_language_supported('kn')


def test_should_not_support_given_languages():
    assert not is_language_supported('mr')
    assert not is_language_supported('pa')
    assert not is_language_supported('ml')


def test_should_support_given_out_formats_transcript():
    assert is_out_format_supported('TRANSCRIPT')

def test_should_support_given_out_formats_srt():
    assert is_out_format_supported('SRT')

def test_should_not_support_given_out_formats():
    assert not is_out_format_supported('ALTERNATIVES')


def test_should_throw_language_not_implemented_error_on_handle():
    lang = Language(value='mr')
    request = SpeechRecognitionRequest(config=RecognitionConfig(language=lang))
    with pytest.raises(NotImplementedError) as e:
        handle_request(request)

    assert e.value.args[0] == 'Language not implemented yet'


def test_should_not_throw_language_not_implemented_error_on_handle():
    lang = Language(value='en')
    request = SpeechRecognitionRequest(config=RecognitionConfig(language=lang))
    handle_request(request)


def test_should_throw_transcript_not_implemented_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat='ALTERNATIVES'))
    with pytest.raises(NotImplementedError) as e:
        handle_request(request)

    assert e.value.args[0] == 'Transcription Format not implemented yet'


def test_should_not_throw_transcript_not_implemented_error_on_handle_transcript():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat='TRANSCRIPT'))
    handle_request(request)

def test_should_not_throw_transcript_not_implemented_error_on_handle_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat='SRT'))
    handle_request(request)
