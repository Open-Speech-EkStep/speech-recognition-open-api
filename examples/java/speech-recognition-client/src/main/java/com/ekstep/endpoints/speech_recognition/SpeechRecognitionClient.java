package com.ekstep.endpoints.speech_recognition;

import com.google.protobuf.ByteString;
import io.grpc.Channel;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;

import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

public class SpeechRecognitionClient {
    private static final Logger logger = Logger.getLogger(SpeechRecognitionClient.class.getName());

    private final SpeechRecognizerGrpc.SpeechRecognizerBlockingStub blockingStub;

    public SpeechRecognitionClient(Channel channel) {
        blockingStub = SpeechRecognizerGrpc.newBlockingStub(channel);
    }

    public SpeechRecognitionResult transcribeUrlV2() {
        String audioUrl = "https://codmento.com/ekstep/test/changed.wav";
        logger.info("Will try to request " + audioUrl + " ...");
        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setLanguage(Language.newBuilder().setValue(Language.LanguageCode.hi).build())
                .setAudioFormat(RecognitionConfig.AudioFormat.WAV)
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder().setAudioUri(audioUrl).build();
        SpeechRecognitionRequest request = SpeechRecognitionRequest.newBuilder()
                .setAudio(audio)
                .setConfig(config)
                .build();
        SpeechRecognitionResult response;

        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return SpeechRecognitionResult.newBuilder().build();
        }
    }

    public SpeechRecognitionResult transcribeBytesV2() {
        logger.info("Will try to request ...");
        AudioFiles audioFiles = new AudioFiles();
        String file = "/Users/nireshkumarr/Documents/ekstep/speech-recognition-open-api/examples/python/speech-recognition/changed.wav";
        byte[] data2 = audioFiles.readAudioFileData(file);
        ByteString byteString = ByteString.copyFrom(data2);

        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setLanguage(Language.newBuilder().setValue(Language.LanguageCode.hi).build())
                .setAudioFormat(RecognitionConfig.AudioFormat.WAV)
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder().setAudioContent(byteString).build();
        SpeechRecognitionRequest request = SpeechRecognitionRequest.newBuilder()
                .setAudio(audio)
                .setConfig(config)
                .build();

        SpeechRecognitionResult response;
        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return SpeechRecognitionResult.newBuilder().build();
        }
    }

    public SpeechRecognitionResult srtUrlV2() {
        String audioUrl = "https://codmento.com/ekstep/test/changed.wav";
        logger.info("Will try to request " + audioUrl + " ...");
        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setLanguage(Language.newBuilder().setValue(Language.LanguageCode.hi).build())
                .setAudioFormat(RecognitionConfig.AudioFormat.WAV)
                .setTranscriptionFormat(RecognitionConfig.TranscriptionFormat.SRT)
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder().setAudioUri(audioUrl).build();
        SpeechRecognitionRequest request = SpeechRecognitionRequest.newBuilder()
                .setAudio(audio)
                .setConfig(config)
                .build();
        SpeechRecognitionResult response;

        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return SpeechRecognitionResult.newBuilder().build();
        }
    }



    public SpeechRecognitionResult srtBytesV2() {
        logger.info("Will try to request ...");
        AudioFiles audioFiles = new AudioFiles();
        String file = "/Users/nireshkumarr/Documents/ekstep/speech-recognition-open-api/examples/python/speech-recognition/changed.wav";
        byte[] data2 = audioFiles.readAudioFileData(file);
        ByteString byteString = ByteString.copyFrom(data2);

        RecognitionConfig config = RecognitionConfig.newBuilder()
                .setLanguage(Language.newBuilder().setValue(Language.LanguageCode.hi).build())
                .setAudioFormat(RecognitionConfig.AudioFormat.WAV)
                .setTranscriptionFormat(RecognitionConfig.TranscriptionFormat.SRT)
                .build();
        RecognitionAudio audio = RecognitionAudio.newBuilder().setAudioContent(byteString).build();
        SpeechRecognitionRequest request = SpeechRecognitionRequest.newBuilder()
                .setAudio(audio)
                .setConfig(config)
                .build();

        SpeechRecognitionResult response;
        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return SpeechRecognitionResult.newBuilder().build();
        }
    }

    public static void main(String[] args) throws Exception {
        String target = "34.70.114.226:50051";

        ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
                .usePlaintext()
                .build();
        try {
            SpeechRecognitionClient client = new SpeechRecognitionClient(channel);
            SpeechRecognitionResult srtUrlResponse = client.srtUrlV2()
            SpeechRecognitionResult srtBytesResponse = client.srtBytesV2();
            SpeechRecognitionResult bytesResponse = client.transcribeBytesV2();
            SpeechRecognitionResult urlResponse = client.transcribeUrlV2();
            System.out.println(bytesResponse.getTranscript());
            System.out.println(urlResponse.getTranscript());
            System.out.println(srtBytesResponse.getSrt());
            System.out.println(srtUrlResponse.getSrt());

        } finally {
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
