import subprocess
from pathlib import Path
from pydub import AudioSegment

from src.utilities import clip_audio


def media_conversion(file=Path, duration_limit=5):
    dir_name = file.parent
    subprocess.call(["ffmpeg -i {} -ar {} -ac {} -bits_per_raw_sample {} -vn {}".format(file, 16000, 1, 16,
                                                                                        dir_name / 'input_audio.wav')],
                    shell=True)
    audio_file = AudioSegment.from_wav(dir_name / 'input_audio.wav')
    clip_audio(audio_file, dir_name, duration_limit)

    return dir_name
