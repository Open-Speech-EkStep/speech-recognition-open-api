from pydub import AudioSegment, effects


class AudioNormalization:
    def __init__(self, wav_file):
        self.wav_file = wav_file

    def loudness_normalization(self, target_dBFS=-15):
        audio_file = AudioSegment.from_file(self.wav_file, format='wav')
        loudness_difference = target_dBFS - audio_file.dBFS
        normalized_audio = audio_file + loudness_difference
        return normalized_audio

    def loudness_normalization_effects(self):
        audio_file = AudioSegment.from_file(self.wav_file, format='wav')
        normalized_audio = effects.normalize(audio_file)
        return normalized_audio