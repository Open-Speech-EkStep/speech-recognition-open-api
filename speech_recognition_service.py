import os, requests

from model_service import ModelService
from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import SpeechRecognitionResult, Language, RecognitionConfig
from utilities import download_from_url_to_file, create_wav_file_using_bytes, get_current_time_in_millis
from speech_recognition_service_handler import handle_request


# add error message field to status
# handle grpc thrown error from server
# move default field of Model field to 0 from 3
class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):

    def __init__(self):
        model_dict_path = "model_dict.json"
        self.model_service = ModelService(model_dict_path)
        print("Loaded successfully")

    def recognize(self, request, context):
        handle_request(request)
        punctuate = request.config.punctuate
        print("***",punctuate)
        language = Language.LanguageCode.Name(request.config.language.value)
        audio_format = RecognitionConfig.AudioFormat.Name(request.config.audioFormat)
        out_format = RecognitionConfig.TranscriptionFormat.Name(request.config.transcriptionFormat)
        file_name = 'audio_input_{}.{}'.format(str(get_current_time_in_millis()), audio_format.lower())
        try:
            if len(request.audio.audioUri) != 0:
                audio_path = download_from_url_to_file(file_name, request.audio.audioUri)
            elif len(request.audio.audioContent) != 0:
                audio_path = create_wav_file_using_bytes(file_name, request.audio.audioContent)
            if out_format == 'SRT':
                response = self.model_service.get_srt(audio_path, language)
                result = SpeechRecognitionResult(status='SUCCESS', srt=response['srt'])
            else:
                response = self.model_service.transcribe(audio_path, language, punctuate)
                result = SpeechRecognitionResult(status='SUCCESS', transcript=response['transcription'])
            os.remove(audio_path)
            return result
        except requests.exceptions.RequestException as e:
            raise RuntimeError(e)
        except Exception as e:
            raise RuntimeError("An unknown error has occurred.Please try again.")
