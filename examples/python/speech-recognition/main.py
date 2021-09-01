import grpc
from stub.speech_recognition_open_api_pb2_grpc import SpeechRecognizerStub
from stub.speech_recognition_open_api_pb2 import Language, RecognitionConfig, RecognitionAudio, \
    SpeechRecognitionRequest
import wave


# from grpc_interceptor import ClientCallDetails, ClientInterceptor


class GrpcAuth(grpc.AuthMetadataPlugin):
    def __init__(self, key):
        self._key = key

    def __call__(self, context, callback):
        callback((('rpc-auth-header', self._key),), None)


# class MetadataClientInterceptor(ClientInterceptor):
#
#     def __init__(self, key):
#         self._key = key
#
#     def intercept(
#             self,
#             method,
#             request_or_iterator,
#             call_details: grpc.ClientCallDetails,
#     ):
#         new_details = ClientCallDetails(
#             call_details.method,
#             call_details.timeout,
#             [("authorization", "Bearer " + self._key)],
#             call_details.credentials,
#             call_details.wait_for_ready,
#             call_details.compression,
#         )
#
#         return method(request_or_iterator, new_details)


def read_audio():
    with wave.open('changed.wav', 'rb') as f:
        return f.readframes(f.getnframes())


def transcribe_audio_bytes(stub):
    language = "mr"
    audio_bytes = read_audio()
    lang = Language(value=language, name='Marathi')
    config = RecognitionConfig(language=lang, transcriptionFormat='TRANSCRIPT',
                               enableAutomaticPunctuation=1)
    audio = RecognitionAudio(audioContent=audio_bytes)
    request = SpeechRecognitionRequest(audio=audio, config=config)

    # creds = grpc.metadata_call_credentials(
    #     metadata_plugin=GrpcAuth('access_key')
    # )
    try:
        response = stub.recognize(request)

        print(response.transcript)
    except grpc.RpcError as e:
        e.details()
        status_code = e.code()
        print(status_code.name)
        print(status_code.value)


def transcribe_audio_url(stub):
    language = "hi"
    url = "https://codmento.com/ekstep/test/changed.wav"
    lang = Language(value=language, name='Hindi')
    config = RecognitionConfig(language=lang, enableAutomaticPunctuation=True)
    audio = RecognitionAudio(audioUri=url)
    request = SpeechRecognitionRequest(audio=audio, config=config)

    response = stub.recognize(request)

    print(response.transcript)


def get_srt_audio_bytes(stub):
    language = "hi"
    audio_bytes = read_audio()
    lang = Language(value=language, name='Hindi')
    config = RecognitionConfig(language=lang, audioFormat='WAV', transcriptionFormat='SRT',
                               enableInverseTextNormalization=True, enableAutomaticPunctuation=True)
    audio = RecognitionAudio(audioContent=audio_bytes)
    request = SpeechRecognitionRequest(audio=audio, config=config)

    # creds = grpc.metadata_call_credentials(
    #     metadata_plugin=GrpcAuth('access_key')
    # )
    response = stub.recognize(request)

    print(response.srt)


def get_srt_audio_url(stub):
    language = "gu"
    url = "https://codmento.com/ekstep/test/changed.wav"
    lang = Language(value=language, name='Gujarati')
    config = RecognitionConfig(language=lang, audioFormat='WAV', transcriptionFormat='SRT')
    audio = RecognitionAudio(audioUri=url)
    request = SpeechRecognitionRequest(audio=audio, config=config)

    response = stub.recognize(request)

    print(response.srt)


if __name__ == '__main__':
    key = "mysecrettoken"
    # interceptors = [MetadataClientInterceptor(key)]
    with grpc.insecure_channel('35.202.181.234:50051') as channel:
        # channel = grpc.intercept_channel(channel, *interceptors)
        stub = SpeechRecognizerStub(channel)
        # transcribe_audio_url(stub)
        # transcribe_audio_bytes(stub)
        # get_srt_audio_url(stub)
        get_srt_audio_bytes(stub)
