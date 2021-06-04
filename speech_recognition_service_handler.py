from stub.speech_recognition_open_api_pb2 import RecognitionConfig, Language


def handle_request(request):
    language = Language.LanguageCode.Name(request.config.language.value)
    if not is_language_supported(language):
        raise NotImplementedError('Language not implemented yet')
    punctuate = request.config.punctuate
    if not is_language_punctuation_supported(language, punctuate):
        raise NotImplementedError('Language and punctuation not implemented yet. Only Hindi and English is supported.')
    itn = request.config.itn
    if not is_language_itn_supported(language, itn):
        raise NotImplementedError('Language and itn not implemented yet. Only Hindi and English is supported.')
    out_format = RecognitionConfig.TranscriptionFormat.Name(request.config.transcriptionFormat)
    if not is_out_format_supported(out_format):
        raise NotImplementedError('Transcription Format not implemented yet')
    audio_format = RecognitionConfig.AudioFormat.Name(request.config.audioFormat)
    if not is_audio_format_supported(audio_format):
        raise NotImplementedError('Audio Format not implemented yet')
    if not is_audio_format_and_out_format_supported(audio_format, out_format):
        raise NotImplementedError('Audio Format and Transcription Format combination not implemented yet')
    audio_source_valid_flag, err_msg = check_audio_source_valid(request.audio)
    if not audio_source_valid_flag:
        raise NotImplementedError(err_msg)


def is_language_supported(language):
    return language in ['hi', 'ta', 'te', 'kn', 'or', 'gu', 'en']


def is_language_punctuation_supported(language, punctuate):
    if punctuate:
        return language in ['hi', 'en']
    else:
        return True


def is_language_itn_supported(language, itn):
    if itn:
        return language in ['hi', 'en']
    else:
        return True


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


def check_audio_source_valid(audioconfigobj):
    if len(getattr(audioconfigobj, 'audioUri', '')) == 0:
        if len(getattr(audioconfigobj, 'audioContent', b'')) == 0:
            if len(getattr(audioconfigobj, 'fileId', '')) == 0:
                return False, 'empty audio source is not implemented yet, send valid attributes only for audioUri or audioContent'
            else:
                return False, 'fileId is not implemented yet'
        else:
            return True, ''
    else:
        return True, ''
