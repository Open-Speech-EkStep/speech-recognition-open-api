from stub.speech_recognition_open_api_pb2 import RecognitionConfig, Language


def handle_request(request):
    language = Language.LanguageCode.Name(request.config.language.value)
    if not is_language_supported(language):
        raise NotImplementedError('Language not implemented yet')
    out_format = RecognitionConfig.TranscriptionFormat.Name(request.config.transcriptionFormat)
    if not is_out_format_supported(out_format):
        raise NotImplementedError('Transcription Format not implemented yet')
    audio_format = RecognitionConfig.AudioFormat.Name(request.config.audioFormat)
    if not is_audio_format_supported(audio_format):
        raise NotImplementedError('Audio Format not implemented yet')
    if not is_audio_format_and_out_format_supported(audio_format, out_format):
        raise NotImplementedError('Audio Format and Transcription Format combination not implemented yet')


def is_language_supported(language):
    return language in ['en', 'hi', 'ta', 'te', 'kn', 'or', 'gu', 'en-IN']


def is_out_format_supported(out_format):
    return out_format in ['TRANSCRIPT', 'SRT']


def is_audio_format_supported(audio_format):
    return audio_format in ['WAV', 'MP3', 'PCM']


def is_audio_format_and_out_format_supported(audio_format, out_format):
    if out_format == 'TRANSCRIPT' and audio_format == 'WAV':
        return True
    elif out_format == 'SRT' and audio_format in ['WAV', 'MP3', 'PCM']:
        return True
    return False
