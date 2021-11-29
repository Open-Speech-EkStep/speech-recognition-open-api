import os
import time
import wave

import requests


def validate_content(response, audio_format='wav'):
    supported_content_length = os.environ.get('supported_content_length', 3145728)
    supported_content_types = ['audio', 'video']
    content_type = response.headers.get('Content-Type')
    content_length = response.headers.get('Content-Length', len(response.content))
    if content_type is None or not content_type.startswith(tuple(supported_content_types)):
        raise ValueError("Invalid audio input format. Only supported formats are allowed.")
    if not content_type.endswith(audio_format):
        raise ValueError("Mismatch between audio format specified and audio format of file specified.")
    if content_length > supported_content_length:
        raise ValueError(f"Audio input size exceeds limit of {supported_content_length} bytes.")
    if content_length == 0:
        raise ValueError(f"Audio input size is 0.")


def download_from_url_to_file(file_name, url, audio_format):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    validate_content(response, audio_format.lower())
    with open(file_name, 'wb') as f:
        f.write(response.content)
    return os.path.join(os.getcwd(), file_name)


def create_wav_file_using_bytes(file_name, audio):
    with wave.open(file_name, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(16000.0)
        file.writeframes(audio)
    return os.path.join(os.getcwd(), file_name)


def write_to_file(file_name, audio):
    with open(file_name, 'wb') as f:
        f.write(audio)
    return os.path.join(os.getcwd(), file_name)


def convert_audio_to_required_format(file_name):
    pass


def get_current_time_in_millis():
    return round(time.time() * 1000)
