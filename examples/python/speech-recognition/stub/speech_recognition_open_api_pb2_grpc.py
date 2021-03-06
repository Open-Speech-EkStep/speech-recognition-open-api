# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import stub.speech_recognition_open_api_pb2 as speech__recognition__open__api__pb2


class SpeechRecognizerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.recognize_audio = channel.stream_stream(
                '/ekstep.speech_recognition.SpeechRecognizer/recognize_audio',
                request_serializer=speech__recognition__open__api__pb2.Message.SerializeToString,
                response_deserializer=speech__recognition__open__api__pb2.Response.FromString,
                )
        self.punctuate = channel.unary_unary(
                '/ekstep.speech_recognition.SpeechRecognizer/punctuate',
                request_serializer=speech__recognition__open__api__pb2.PunctuateRequest.SerializeToString,
                response_deserializer=speech__recognition__open__api__pb2.PunctuateResponse.FromString,
                )
        self.recognize = channel.unary_unary(
                '/ekstep.speech_recognition.SpeechRecognizer/recognize',
                request_serializer=speech__recognition__open__api__pb2.SpeechRecognitionRequest.SerializeToString,
                response_deserializer=speech__recognition__open__api__pb2.SpeechRecognitionResult.FromString,
                )


class SpeechRecognizerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def recognize_audio(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def punctuate(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def recognize(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SpeechRecognizerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'recognize_audio': grpc.stream_stream_rpc_method_handler(
                    servicer.recognize_audio,
                    request_deserializer=speech__recognition__open__api__pb2.Message.FromString,
                    response_serializer=speech__recognition__open__api__pb2.Response.SerializeToString,
            ),
            'punctuate': grpc.unary_unary_rpc_method_handler(
                    servicer.punctuate,
                    request_deserializer=speech__recognition__open__api__pb2.PunctuateRequest.FromString,
                    response_serializer=speech__recognition__open__api__pb2.PunctuateResponse.SerializeToString,
            ),
            'recognize': grpc.unary_unary_rpc_method_handler(
                    servicer.recognize,
                    request_deserializer=speech__recognition__open__api__pb2.SpeechRecognitionRequest.FromString,
                    response_serializer=speech__recognition__open__api__pb2.SpeechRecognitionResult.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ekstep.speech_recognition.SpeechRecognizer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SpeechRecognizer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def recognize_audio(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/ekstep.speech_recognition.SpeechRecognizer/recognize_audio',
            speech__recognition__open__api__pb2.Message.SerializeToString,
            speech__recognition__open__api__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def punctuate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ekstep.speech_recognition.SpeechRecognizer/punctuate',
            speech__recognition__open__api__pb2.PunctuateRequest.SerializeToString,
            speech__recognition__open__api__pb2.PunctuateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def recognize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ekstep.speech_recognition.SpeechRecognizer/recognize',
            speech__recognition__open__api__pb2.SpeechRecognitionRequest.SerializeToString,
            speech__recognition__open__api__pb2.SpeechRecognitionResult.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
