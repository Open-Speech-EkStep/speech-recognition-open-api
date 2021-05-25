from stub.speech_recognition_open_api_pb2 import RecognitionConfig, Language


def handle_request(request):
    language = Language.LanguageCode.Name(request.config.language.value)
    if not is_language_supported(language):
        raise NotImplementedError('Language not implemented yet')
    out_format = RecognitionConfig.TranscriptionFormat.Name(request.config.transcriptionFormat)
    if not is_out_format_supported(out_format):
        raise NotImplementedError('Transcription Format not implemented yet')


def is_language_supported(language):
    return language in ['en', 'hi', 'ta', 'te', 'kn', 'or', 'gu', 'en-IN']


def is_out_format_supported(out_format):
    return out_format in ['TRANSCRIPT', 'SRT']
