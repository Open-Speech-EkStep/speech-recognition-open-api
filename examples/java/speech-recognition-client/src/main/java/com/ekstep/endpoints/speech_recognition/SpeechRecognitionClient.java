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

    public RecognitionOutput transcribeUrl() {
        String audioUrl = "https://codmento.com/ekstep/test/changed.wav";
        String language = "hi";
        String fileName = "hindi2.wav";
        logger.info("Will try to request " + audioUrl + " ...");
        RecognitionInput request = RecognitionInput.newBuilder().setFileName(fileName).setAudioUrl(audioUrl).setLanguage(language).build();
        RecognitionOutput response;
        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return RecognitionOutput.newBuilder().build();
        }
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
            response = blockingStub.recognizeV2(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return SpeechRecognitionResult.newBuilder().build();
        }
    }

    public RecognitionOutput transcribeBytes() {
        logger.info("Will try to request ...");
        AudioFiles afiles = new AudioFiles();
        String language = "hi";
        String file = "/Users/nireshkumarr/Documents/ekstep/speech-recognition-open-api/examples/python/speech-recognition/changed.wav";
        byte[] data2 = afiles.readAudioFileData(file);
        ByteString byteString = ByteString.copyFrom(data2);
        String fileName = "hindi2.wav";
        RecognitionInput request = RecognitionInput.newBuilder().setFileName(fileName).setAudioBytes(byteString).setLanguage(language).build();
        RecognitionOutput response;
        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return RecognitionOutput.newBuilder().build();
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
            response = blockingStub.recognizeV2(request);
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
            /* v1 */
            /* RecognitionOutput bytesResponse = client.transcribeBytes();
            RecognitionOutput urlResponse = client.transcribeUrl();
            System.out.println(bytesResponse.getResult());
            System.out.println(urlResponse.getResult()); */

            /* v2 */
            SpeechRecognitionResult bytesResponse = client.transcribeBytesV2();
            SpeechRecognitionResult urlResponse = client.transcribeUrlV2();
            System.out.println(bytesResponse.getTranscript());
            System.out.println(urlResponse.getTranscript());

        } finally {
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
