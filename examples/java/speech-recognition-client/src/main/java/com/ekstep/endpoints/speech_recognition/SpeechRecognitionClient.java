package com.ekstep.endpoints.speech_recognition;

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

    /**
     * Construct client for accessing HelloWorld server using the existing channel.
     */
    public SpeechRecognitionClient(Channel channel) {
        // 'channel' here is a Channel, not a ManagedChannel, so it is not this code's responsibility to
        // shut it down.

        // Passing Channels to code makes code easier to test and makes it easier to reuse Channels.
        blockingStub = SpeechRecognizerGrpc.newBlockingStub(channel);
    }

    /**
     * Say hello to server.
     */
    public RecognitionOutput transcribe(String audioUrl, String language) {
        logger.info("Will try to request " + audioUrl + " ...");
        RecognitionInput request = RecognitionInput.newBuilder().setAudioUrl(audioUrl).setLanguage(language).build();
        RecognitionOutput response;
        try {
            response = blockingStub.recognize(request);
            return response;
        } catch (StatusRuntimeException e) {
            logger.log(Level.WARNING, "RPC failed: {0}", e.getStatus());
            return RecognitionOutput.newBuilder().build();
        }
    }

    /**
     * Greet server. If provided, the first element of {@code args} is the name to use in the
     * greeting. The second argument is the target server.
     */
    public static void main(String[] args) throws Exception {
        // Access a service running on the local machine on port 50051
        String target = "localhost:50051";
        String audioUrl = "https://abcd/a.mp3";
        String language = "hindi";

        // Create a communication channel to the server, known as a Channel. Channels are thread-safe
        // and reusable. It is common to create channels at the beginning of your application and reuse
        // them until the application shuts down.
        ManagedChannel channel = ManagedChannelBuilder.forTarget(target)
                // Channels are secure by default (via SSL/TLS). For the example we disable TLS to avoid
                // needing certificates.
                .usePlaintext()
                .build();
        try {
            SpeechRecognitionClient client = new SpeechRecognitionClient(channel);
            RecognitionOutput response = client.transcribe(audioUrl, language);
            System.out.println(response.getResult());
        } finally {
            // ManagedChannels use resources like threads and TCP connections. To prevent leaking these
            // resources the channel should be shut down when it will no longer be used. If it may be used
            // again leave it running.
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        }
    }
}
