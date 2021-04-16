package com.ekstep.endpoints.speech_recognition;

import java.io.ByteArrayOutputStream;
import java.io.File;

import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;

public class AudioFiles {
    public static void main(String[] args) {
        String file = "clarinet.wav";
        AudioFiles afiles = new AudioFiles();
        byte[] data1 = afiles.readAudioFileData(file);
        byte[] data2 = afiles.readWAVAudioFileData(file);
        System.out.format("data len: %d\n", data1.length);
        System.out.format("data len: %d\n", data2.length);
        System.out.format("diff len: %d\n", data2.length - data1.length);
    }

    public byte[] readAudioFileData(final String filePath) {
        byte[] data = null;
        try {
            final ByteArrayOutputStream baout = new ByteArrayOutputStream();
            final File file = new File(filePath);
            final AudioInputStream audioInputStream = AudioSystem
                    .getAudioInputStream(file);

            byte[] buffer = new byte[4096];
            int c;
            while ((c = audioInputStream.read(buffer, 0, buffer.length)) != -1) {
                baout.write(buffer, 0, c);
            }
            audioInputStream.close();
            baout.close();
            data = baout.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return data;
    }

    public byte[] readWAVAudioFileData(final String filePath) {
        byte[] data = null;
        try {
            final ByteArrayOutputStream baout = new ByteArrayOutputStream();
            final AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File(filePath));

            AudioSystem.write(audioInputStream, AudioFileFormat.Type.WAVE, baout);
            audioInputStream.close();
            baout.close();
            data = baout.toByteArray();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return data;
    }
}
