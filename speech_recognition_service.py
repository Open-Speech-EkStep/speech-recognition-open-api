import os

import grpc
import requests

from model_service import ModelService
from speech_recognition_service_handler import handle_request
from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import SpeechRecognitionResult, Language, RecognitionConfig
from utilities import download_from_url_to_file, create_wav_file_using_bytes, get_current_time_in_millis


# add error message field to status
# handle grpc thrown error from server
# move default field of Model field to 0 from 3
class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):
    MODEL_BASE_PATH = os.environ.get('models_base_path', '')
    def __init__(self):
        gpu = os.environ.get('gpu', False)
        for path, dirs, files in os.walk(self.MODEL_BASE_PATH):
            print(path)
            for f in files:
                print(f)
        self.model_service = ModelService(self.MODEL_BASE_PATH, 'kenlm', gpu, False)
        print("Loaded models successfully")

    def recognize(self, request, context):
        try:
            handle_request(request, self.model_service.supported_languages)
        except NotImplementedError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return SpeechRecognitionResult(status='ERROR', status_text=str(e))

        punctuate = request.config.enableAutomaticPunctuation
        itn = request.config.enableInverseTextNormalization
        language = Language.LanguageCode.Name(request.config.language.sourceLanguage)
        audio_format = RecognitionConfig.AudioFormat.Name(request.config.audioFormat)
        out_format = RecognitionConfig.TranscriptionFormatEnum.Name(request.config.transcriptionFormat.value)
        model_output_list = []
        for audio_obj in request.audio:
            file_name = 'audio_input_{}.{}'.format(str(get_current_time_in_millis()), audio_format.lower())
            try:
                if len(audio_obj.audioUri) != 0:
                    audio_path = download_from_url_to_file(file_name, audio_obj.audioUri)
                elif len(audio_obj.audioContent) != 0:
                    audio_path = create_wav_file_using_bytes(file_name, audio_obj.audioContent)
                if out_format == 'srt':
                    response = self.model_service.get_srt(audio_path, language, punctuate, itn)
                    output = SpeechRecognitionResult.Output(source=response['srt'])
                    model_output_list.append(output)

                else:
                    response = self.model_service.transcribe(audio_path, language, punctuate, itn)
                    output = SpeechRecognitionResult.Output(source=response['transcription'])
                    model_output_list.append(output)
                os.remove(audio_path)

            except requests.exceptions.RequestException as e:
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return SpeechRecognitionResult(status='ERROR', status_text=str(e))
            except Exception as e:
                context.set_details("An unknown error has occurred.Please try again.")
                context.set_code(grpc.StatusCode.UNKNOWN)
                return SpeechRecognitionResult(status='ERROR',
                                               status_text="An unknown error has occurred.Please try again.")
        result = SpeechRecognitionResult(status='SUCCESS', output=model_output_list)
        return result
