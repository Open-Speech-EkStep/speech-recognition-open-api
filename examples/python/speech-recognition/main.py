import grpc
from proto_lib.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
from proto_lib.speech_recognition_open_api_pb2 import RecognitionInput

with grpc.insecure_channel('localhost:50051') as channel:
    stub = SpeechRecognizerStub(channel)
    url = "https://teest/s.mp3"
    response = stub.recognize(RecognitionInput(audio_url=url))
    print("Successfully requested and response received" if response.result == url else "Not working ! Check again")
    # print(response.result)
