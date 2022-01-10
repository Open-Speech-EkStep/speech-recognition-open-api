import pytest

from src.speech_recognition_service_handler import is_out_format_supported, is_audio_format_supported, \
    is_language_supported, handle_request
from stub.speech_recognition_open_api_pb2 import RecognitionConfig, RecognitionAudio, Language, SpeechRecognitionRequest


def test_should_support_given_languages():
    assert is_language_supported('en')
    assert is_language_supported('en')
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


def test_should_support_given_out_formats():
    assert is_out_format_supported('TRANSCRIPT')
    assert is_out_format_supported('SRT')


def test_should_support_given_audio_formats():
    assert is_audio_format_supported('WAV')
    assert is_audio_format_supported('MP3')
    assert is_audio_format_supported('PCM')


def test_should_not_support_given_audio_formats():
    assert not is_audio_format_supported('OGG')


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
    request = SpeechRecognitionRequest(config=RecognitionConfig(language=lang),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    handle_request(request)


def test_should_throw_transcript_not_implemented_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat='ALTERNATIVES'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    with pytest.raises(NotImplementedError) as e:
        handle_request(request)

    assert e.value.args[0] == 'Transcription Format not implemented yet'


def test_should_not_throw_transcript_not_implemented_error_on_handle_transcript():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat='TRANSCRIPT'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    handle_request(request)


def test_should_not_throw_transcript_not_implemented_error_on_handle_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat='SRT'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    handle_request(request)


def test_should_not_throw_audio_format_not_implemented_error_on_handle_wav():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='WAV'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    handle_request(request)


def test_should_not_throw_audio_and_transcript_format_not_implemented_error_on_handle_mp3_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='MP3', transcriptionFormat='SRT'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    handle_request(request)


def test_should_not_throw_audio_and_transcript_format_not_implemented_error_on_handle_pcm_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='PCM', transcriptionFormat='SRT'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    handle_request(request)


def test_should_throw_audio_format_not_implemented_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='OGG'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    with pytest.raises(NotImplementedError) as e:
        handle_request(request)

    assert e.value.args[0] == 'Audio Format not implemented yet'


def test_should_throw_audio_and_transcript_format_not_implemented_error_on_handle_ogg_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='OGG', transcriptionFormat='SRT'),
                                       audio=RecognitionAudio(audioUri='www.abc.com/demo.wav'))
    with pytest.raises(NotImplementedError) as e:
        handle_request(request)

    assert e.value.args[0] == 'Audio Format not implemented yet'


def test_should_throw_empty_audio_source_is_not_implemented_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='MP3')
                                       )
    with pytest.raises(NotImplementedError) as e:
        handle_request(request)

    assert e.value.args[
               0] == 'empty audio source is not implemented yet, send valid attributes only for audioUri or audioContent'


