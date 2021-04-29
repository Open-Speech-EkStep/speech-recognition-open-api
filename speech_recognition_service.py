from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import SpeechRecognitionResult, Language, RecognitionConfig
from utilities import download_from_url_to_file, create_wav_file_using_bytes, get_current_time_in_millis
import os
from model_service import ModelService


class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):

    def __init__(self):
        model_dict_path = "model_dict.json"
        self.model_service = ModelService(model_dict_path)
        print("Loaded successfully")

    def recognize(self, request, context):
        language = Language.LanguageCode.Name(request.config.language.value)
        audio_format = RecognitionConfig.AudioFormat.Name(request.config.audioFormat)
        file_name = 'audio_input_{}.{}'.format(str(get_current_time_in_millis()), audio_format.lower())
        if len(request.audio.audioUri) != 0:
            audio_path = download_from_url_to_file(file_name, request.audio.audioUri)
        elif len(request.audio.fileId) != 0:
            return SpeechRecognitionResult(status='NO_MATCH')
        else:
            audio_path = create_wav_file_using_bytes(file_name, request.audio.audioContent)
        response = self.model_service.transcribe(audio_path, language)
        os.remove(audio_path)
        return SpeechRecognitionResult(status='SUCCESS', transcript=response['transcription'])
