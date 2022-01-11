package com.ekstep.endpoints.speech_recognition;

import com.google.protobuf.ByteString;
import io.grpc.*;
import io.grpc.stub.MetadataUtils;

import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SpeechRecognitionClient {
    private static final Logger logger = Logger.getLogger(SpeechRecognitionClient.class.getName());

    private final SpeechRecognizerGrpc.SpeechRecognizerBlockingStub blockingStub;

    public SpeechRecognitionClient(Channel channel) {
        blockingStub = SpeechRecognizerGrpc.newBlockingStub(channel);
    }

    public SpeechRecognitionResult transcribeAudioBytes(ByteString audioBytes, Language.LanguageCode language, RecognitionConfig.AudioFormat audioFormat, RecognitionConfig.TranscriptionFormatEnum transcriptionFormat) {
        logger.info("Will try to request ...");

        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setLanguage(Language.newBuilder().setSourceLanguage(language).build())
                .setAudioFormat(audioFormat)
                .setTranscriptionFormat(RecognitionConfig.TranscriptionFormat.newBuilder().setValue(transcriptionFormat).build())
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder().setAudioContent(audioBytes).build();
        SpeechRecognitionRequest request = SpeechRecognitionRequest.newBuilder()
                .addAudio(audio)
                .setConfig(config)
                .build();

        Metadata metadata = new Metadata();
        Metadata.Key<String> key = Metadata.Key.of("language", Metadata.ASCII_STRING_MARSHALLER);
        metadata.put(key, language.toString());

        MetadataUtils.attachHeaders(blockingStub, metadata);

        SpeechRecognitionResult response;
        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return SpeechRecognitionResult.newBuilder().build();
        }
    }

    public static ByteString getAudioBytes() {
        AudioFiles audioFiles = new AudioFiles();
        String file = "/Users/nireshkumarr/Documents/ekstep/speech-recognition-open-api/examples/python/speech-recognition/changed.wav";
        byte[] data2 = audioFiles.readAudioFileData(file);
        ByteString byteString = ByteString.copyFrom(data2);
        return byteString;
    }

    public static void main(String[] args) throws Exception {
        String target = "test-model-api.vakyansh.in:50051";

        ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
                .usePlaintext()
                .build();
        try {
            SpeechRecognitionClient client = new SpeechRecognitionClient(channel);
            ByteString audioBytes = getAudioBytes();
            SpeechRecognitionResult result = client.transcribeAudioBytes(audioBytes, Language.LanguageCode.en, RecognitionConfig.AudioFormat.wav, RecognitionConfig.TranscriptionFormatEnum.transcript);
            System.out.println(result.toString());

        } finally {
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
