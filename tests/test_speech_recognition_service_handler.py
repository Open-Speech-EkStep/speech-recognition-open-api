from path_setter import set_root_folder_path
set_root_folder_path()
import pytest

from src.speech_recognition_service_handler import is_out_format_supported, is_audio_format_supported, \
    is_language_supported, handle_request
from stub.speech_recognition_open_api_pb2 import RecognitionConfig, RecognitionAudio, Language, SpeechRecognitionRequest


def test_should_support_given_languages():
    assert is_language_supported('en', ['en', 'hi'])
    assert is_language_supported('en', ['en', 'hi'])
    assert is_language_supported('hi', ['en', 'hi'])
    assert is_language_supported('ta', ['en', 'ta'])
    assert is_language_supported('te', ['te', 'hi'])
    assert is_language_supported('gu', ['en', 'gu'])
    assert is_language_supported('or', ['or', 'hi'])
    assert is_language_supported('kn', ['en', 'kn'])


def test_should_not_support_given_languages():
    assert not is_language_supported('mr', ['en', 'hi'])
    assert not is_language_supported('pa', ['en', 'hi'])
    assert not is_language_supported('ml', ['en', 'hi'])


def test_should_support_given_out_formats():
    assert is_out_format_supported('transcript')
    assert is_out_format_supported('srt')


def test_should_support_given_audio_formats():
    assert is_audio_format_supported('wav')
    assert is_audio_format_supported('mp3')
    assert is_audio_format_supported('flac')


def test_should_not_support_given_audio_formats():
    assert not is_audio_format_supported('ogg')


def test_should_not_support_given_out_formats():
    assert not is_out_format_supported('alternatives')


def test_should_throw_language_not_implemented_error_on_handle():
    lang = Language(sourceLanguage='mr')
    request = SpeechRecognitionRequest(config=RecognitionConfig(language=lang))
    with pytest.raises(NotImplementedError) as e:
        handle_request(request, ["en", "hi"])

    assert e.value.args[0] == 'Language mr not implemented yet'


def test_should_not_throw_language_not_implemented_error_on_handle():
    lang = Language(sourceLanguage='en')
    request = SpeechRecognitionRequest(config=RecognitionConfig(language=lang),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    handle_request(request, ["en", "hi"])


def test_should_throw_transcript_not_implemented_error_on_handle():
    lang = Language(sourceLanguage='en')
    request = SpeechRecognitionRequest(config=RecognitionConfig(language=lang, transcriptionFormat={'value':'alternatives'}),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    with pytest.raises(NotImplementedError) as e:
        handle_request(request, ["en", "hi"])

    assert e.value.args[0] == 'Transcription Format not implemented yet'


def test_should_not_throw_transcript_not_implemented_error_on_handle_transcript():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat={'value':'transcript'}),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    handle_request(request, ["en", "hi"])


def test_should_not_throw_transcript_not_implemented_error_on_handle_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(transcriptionFormat={'value':'srt'}),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    handle_request(request, ["en", "hi"])


def test_should_not_throw_audio_format_not_implemented_error_on_handle_wav():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='wav'),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    handle_request(request, ["en", "hi"])


def test_should_not_throw_audio_and_transcript_format_not_implemented_error_on_handle_mp3_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='mp3', transcriptionFormat={'value':'srt'}),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    handle_request(request, ["en", "hi"])


def test_should_not_throw_audio_and_transcript_format_not_implemented_error_on_handle_flac_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='flac', transcriptionFormat={'value':'srt'}),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    handle_request(request, ["en", "hi"])


def test_should_throw_audio_format_not_implemented_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='pcm'),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    with pytest.raises(NotImplementedError) as e:
        handle_request(request, ["en", "hi"])

    assert e.value.args[0] == 'Audio Format not implemented yet'


def test_should_throw_audio_and_transcript_format_not_implemented_error_on_handle_pcm_srt():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='pcm', transcriptionFormat={'value':'srt'}),
                                       audio=[RecognitionAudio(audioUri='www.abc.com/demo.wav')])
    with pytest.raises(NotImplementedError) as e:
        handle_request(request, ["en", "hi"])

    assert e.value.args[0] == 'Audio Format not implemented yet'

def test_should_throw_audio_input_not_specified_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='mp3')
                                       )
    with pytest.raises(ValueError) as e:
        handle_request(request, ["en", "hi"])

    assert e.value.args[0] == 'Audio input not specified'

def test_should_throw_empty_audio_source_is_not_implemented_error_on_handle():
    request = SpeechRecognitionRequest(config=RecognitionConfig(audioFormat='mp3'), audio=[RecognitionAudio()])
    with pytest.raises(NotImplementedError) as e:
        handle_request(request, ["en", "hi"])

    assert e.value.args[
               0] == 'empty audio source is not implemented yet, send valid attributes only for audioUri or audioContent'


