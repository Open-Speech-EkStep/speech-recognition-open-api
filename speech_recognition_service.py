from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import RecognitionOutput
from utilities import download_from_url_to_file,create_wav_file_using_bytes,write_to_file
from model_service import ModelService

class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):

    def __init__(self):
        model_dict_path = "./../wav2vec_vakyansh/model_dict.json"
        self.model_service = ModelService(model_dict_path)
        print("Loaded successfully")

    def recognize(self, request, context):
        print("Received", request.language, request.file_name)
        if len(request.audio_url) != 0:
            audio_path = download_from_url_to_file(request.file_name, request.audio_url)
        else:
            audio_path = create_wav_file_using_bytes(request.file_name, request.audio_bytes)
        response = self.model_service.transcribe(audio_path, request.language)
        return RecognitionOutput(result=response['transcription'])
        # if len(request.audio_url) != 0:
        #     return RecognitionOutput(result=request.audio_url)
        # else:
        #     return RecognitionOutput(result=str(request.audio_bytes))
