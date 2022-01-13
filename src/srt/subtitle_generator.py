import os
import subprocess

import torch

from src import log_setup
from src.media_convertor import media_conversion
from src.srt.infer import generate_srt

LOGGER = log_setup.get_logger(__name__)


def noise_suppression(dir_name: str, denoiser_path):
    cwd = os.getcwd()
    os.chdir(denoiser_path)
    LOGGER.debug(f'Calling noise suppression from denoiser_path {denoiser_path} on directory {dir_name}')
    subprocess.call([
        "python -m denoiser.enhance --dns48 --noisy_dir {} --out_dir {} --sample_rate {} --num_workers {} --device cpu".format(
            dir_name, dir_name, 16000, 1)], shell=True)
    LOGGER.debug(f'denoiser done')
    os.chdir(cwd)


def get_srt(file, model, generator, dict_path, denoiser_path, audio_threshold=5, language='hi', half=False):
    dir_name = media_conversion(file, duration_limit=audio_threshold)
    LOGGER.debug(f'Media conversion done for file {file}')
    noise_suppression(str(dir_name), denoiser_path)
    audio_file = dir_name / 'clipped_audio_enhanced.wav'
    LOGGER.debug(f'Requesting generate_srt on audio file {audio_file}')
    result = generate_srt(wav_path=audio_file, language=language, model=model, generator=generator,
                          cuda=torch.cuda.is_available(), dict_path=dict_path, half=half)

    return result
