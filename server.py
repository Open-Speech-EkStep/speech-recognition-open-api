from concurrent import futures
import grpc
from src.speech_recognition_service import SpeechRecognizer
from stub.speech_recognition_open_api_pb2_grpc import add_SpeechRecognizerServicer_to_server

from fairseq.models.wav2vec.wav2vec2_asr import Wav2VecCtc


def run():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        # interceptors=(AuthInterceptor('Bearer mysecrettoken'),)
    )
    add_SpeechRecognizerServicer_to_server(SpeechRecognizer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    run()
