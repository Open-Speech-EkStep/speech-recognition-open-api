import os
import time
import uuid
import wave

import requests
from mimeparse import parse_mime_type

from src.monitoring import monitor


def validate_content(response, audio_format='wav'):
    audio_content_type_extension_map = {"mp3": ["mp3", "mpeg"], "wav": ["wav", "x-wav", "vnd.wav"],
                                        "flac": ["x-flac", "flac"], }
    supported_content_length = get_env_var('supported_content_length', 3145728)
    supported_content_types = ['audio']
    content_type = response.headers.get('Content-Type')
    content_length = response.headers.get('Content-Length', len(response.content))
    if content_type is None:
        raise ValueError("Invalid audio input format. Only supported formats are allowed.")

    try:
        content_type_value, subtype, options = parse_mime_type(content_type)
    except:
        raise ValueError("Invalid audio url (No mimetype present).")

    if not content_type_value in supported_content_types:
        raise ValueError("Invalid audio input format. Only supported formats are allowed.")
    if not subtype in audio_content_type_extension_map[audio_format]:
        raise ValueError("Mismatch between audio format specified and audio format of file given.")
    if int(content_length) > supported_content_length:
        raise ValueError(f"Audio input size exceeds limit of {supported_content_length} bytes.")
    if int(content_length) == 0:
        raise ValueError(f"Audio input size is 0.")


@monitor
def download_from_url_to_file(file, url, audio_format):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    validate_content(response, audio_format.lower())
    with open(file, 'wb') as f:
        f.write(response.content)
    return file


def create_wav_file_using_bytes(file, audio):
    with wave.open(file, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(16000.0)
        file.writeframes(audio)
    return file


@monitor
def write_to_file(file_name, audio):
    with open(file_name, 'wb') as f:
        f.write(audio)
    return os.path.join(os.getcwd(), file_name)


def convert_audio_to_required_format(file_name):
    pass


def get_current_time_in_millis():
    return round(time.time() * 1000)


def create_directory(file):
    if not os.path.exists(file):
        os.makedirs(file)


def delete_file(file):
    if os.path.exists(file):
        os.remove(file)


def get_env_var(var_name=str, default=''):
    return os.environ.get(var_name, default)


def create_temp_dir():
    temp_dir = os.path.join('/tmp', uuid.uuid4().hex)
    create_directory(temp_dir)
    return temp_dir


def clip_audio(audio_file, dir_name, duration_limit):
    audio_duration_min = audio_file.duration_seconds / 60
    if audio_duration_min > duration_limit:
        d_limit = duration_limit * 60 * 1000
        clipped_audio = audio_file[:d_limit]
        clipped_audio.export(dir_name / 'clipped_audio.wav', format='wav')
    else:
        audio_file.export(dir_name / 'clipped_audio.wav', format='wav')
