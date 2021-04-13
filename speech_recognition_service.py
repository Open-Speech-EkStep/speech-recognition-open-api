from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import RecognitionOutput


class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):
    def recognize(self, request, context):
        if len(request.audio_url) != 0:
            return RecognitionOutput(result=request.audio_url)
        else:
            return RecognitionOutput(result=str(request.audio_bytes))



