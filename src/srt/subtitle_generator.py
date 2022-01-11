import os
import shutil
import subprocess

import torch

from src import log_setup
from src.srt.infer import generate_srt
from src.utilities import media_conversion

LOGGER = log_setup.get_logger(__name__)


def noise_suppression(dir_name, denoiser_path):
    cwd = os.getcwd()
    os.chdir(denoiser_path)
    subprocess.call([
                        "python -m denoiser.enhance --dns48 --noisy_dir {} --out_dir {} --sample_rate {} --num_workers {} --device cpu".format(
                            dir_name, dir_name, 16000, 1)], shell=True)
    os.chdir(cwd)


def get_srt(file, model, generator, dict_path, denoiser_path, audio_threshold=5, language='hi', half=False):
    dir_name = media_conversion(file, duration_limit=audio_threshold)
    noise_suppression(dir_name, denoiser_path)
    audio_file = dir_name + '/clipped_audio_enhanced.wav'

    result = generate_srt(wav_path=audio_file, language=language, model=model, generator=generator,
                          cuda=torch.cuda.is_available(), dict_path=dict_path, half=half)

    return result