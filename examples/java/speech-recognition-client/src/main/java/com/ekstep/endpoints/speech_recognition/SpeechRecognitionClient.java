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


    public static void main(String[] args) throws Exception {
        String target = "34.70.114.226:50051";

        ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
                .usePlaintext()
                .build();
        try {
            SpeechRecognitionClient client = new SpeechRecognitionClient(channel);
            RecognitionOutput response = client.transcribeBytes();
//            RecognitionOutput response = client.transcribeUrl();
            System.out.println(response.getResult());
        } finally {
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
