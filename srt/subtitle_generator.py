import os, datetime
import subprocess
from pydub import AudioSegment
from srt.infer import generate_srt
import torch
import shutil

def media_conversion(file_name, duration_limit=5):
    dir_name = os.path.join('/tmp', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.makedirs(dir_name)

    subprocess.call(["ffmpeg -i {} -ar {} -ac {} -bits_per_raw_sample {} -vn {}".format(file_name, 16000, 1, 16, dir_name + '/input_audio.wav')], shell=True)

    audio_file = AudioSegment.from_wav(dir_name + '/input_audio.wav')

    audio_duration_min = audio_file.duration_seconds / 60

    if audio_duration_min > duration_limit:
        d_limit = duration_limit * 60 * 1000
        clipped_audio = audio_file[:d_limit]
        clipped_audio.export(dir_name + '/clipped_audio.wav', format='wav')
    else:
        audio_file.export(dir_name + '/clipped_audio.wav', format='wav')

    os.remove(dir_name + '/input_audio.wav')

    return dir_name

def noise_suppression(dir_name,denoiser_path):
    cwd = os.getcwd()
    os.chdir(denoiser_path)
    subprocess.call(["python -m denoiser.enhance --dns48 --noisy_dir {} --out_dir {} --sample_rate {} --num_workers {} --device cpu".format(dir_name, dir_name, 16000, 1)], shell=True)
    os.chdir(cwd)

def get_srt(file_name, model, generator, dict_path, denoiser_path, audio_threshold=5, language='hi', half = False):
    dir_name = media_conversion(file_name, duration_limit=audio_threshold)
    noise_suppression(dir_name, denoiser_path)
    audio_file = dir_name + '/clipped_audio_enhanced.wav'

    result = generate_srt(wav_path=audio_file, language=language, model=model, generator=generator, cuda=torch.cuda.is_available(), dict_path=dict_path, half=half)
    
    if os.path.isdir(dir_name):
        shutil.rmtree(dir_name)

    return result

#subtitle_generation('/home/nireshkumarr/test_vad/ravish_short.mp3', audio_threshold=1, language='en-IN')






