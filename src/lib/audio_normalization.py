from pydub import AudioSegment, effects

from src import log_setup

LOGGER = log_setup.get_logger(__name__)


class AudioNormalization:
    def __init__(self, wav_file):
        self.wav_file = wav_file

    def loudness_normalization(self, target_dBFS=-15):
        audio_file = AudioSegment.from_file(self.wav_file, format='wav')
        loudness_difference = target_dBFS - audio_file.dBFS
        normalized_audio = audio_file + loudness_difference
        return normalized_audio

    def loudness_normalization_effects(self):
        LOGGER.debug(f'doing loudness_normalization_effects')
        audio_file = AudioSegment.from_file(self.wav_file, format='wav')
        LOGGER.debug(f'doing loudness_normalization_effects for file {audio_file}')
        normalized_audio = effects.normalize(audio_file)
        LOGGER.debug(f'done loudness_normalization_effects for file {audio_file}')
        return normalized_audio
