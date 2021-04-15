from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import RecognitionOutput
from model_service import ModelService

class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):

    def __init__(self):
        # model_dict_path = "./../wav2vec_vakyansh/model_dict.json"
        # self.model_service = ModelService(model_dict_path)
        # print("Model loaded successfully")
        pass


    def recognize(self, request, context):
        # audio_path = './../wav2vec_vakyansh/xEOIIzS5VySDKU9OAAAB1.wav'
        # language = 'en-IN'
        # if len(request.audio_url) != 0:
        #     response = self.model_service.transcribe(audio_path, language)
        #     return RecognitionOutput(result=response['transcription'])
        # else:
        #     return RecognitionOutput(result=str(request.audio_bytes))
        if len(request.audio_url) != 0:
            return RecognitionOutput(result=request.audio_url)
        else:
            return RecognitionOutput(result=str(request.audio_bytes))



