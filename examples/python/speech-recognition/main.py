import grpc
from stub.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
from stub.speech_recognition_open_api_pb2 import RecognitionInput, Language, RecognitionConfig, RecognitionAudio, \
    SpeechRecognitionRequest
import wave


def read_audio():
    with wave.open('changed.wav', 'rb') as f:
        return f.readframes(f.getnframes())


def transcribe_audio_bytes_v1(stub):
    language = "hi"
    audio = read_audio()
    response = stub.recognize(RecognitionInput(audio_bytes=audio, file_name='hindi1.wav', language=language))
    print(response.result)


def transcribe_audio_url_v1(stub):
    language = "hi"
    url = "https://codmento.com/ekstep/test/changed.wav"
    response = stub.recognize(RecognitionInput(audio_url=url, file_name='hindi2.wav', language=language))
    print(response.result)


def transcribe_audio_bytes_v2(stub):
    language = "hi"
    audio_bytes = read_audio()
    lang = Language(value=language, name='Hindi')
    config = RecognitionConfig(language=lang, audioFormat='WAV')
    audio = RecognitionAudio(audioContent=audio_bytes)
    request = SpeechRecognitionRequest(audio=audio, config=config)

    response = stub.recognizeV2(request)

    print(response.transcript)


def transcribe_audio_url_v2(stub):
    language = "hi"
    url = "https://codmento.com/ekstep/test/changed.wav"
    lang = Language(value=language, name='Hindi')
    config = RecognitionConfig(language=lang, audioFormat='WAV')
    audio = RecognitionAudio(audioUri=url)
    request = SpeechRecognitionRequest(audio=audio, config=config)

    response = stub.recognizeV2(request)

    print(response.transcript)


if __name__ == '__main__':
    with grpc.insecure_channel('34.70.114.226:50051') as channel:
        stub = SpeechRecognizerStub(channel)
        transcribe_audio_bytes_v2(stub)
        transcribe_audio_url_v2(stub)
