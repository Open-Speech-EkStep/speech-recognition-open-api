import os
import time
import wave

import requests
from mimeparse import parse_mime_type

def validate_content(response, audio_format='wav'):
    audio_content_type_extension_map = {"mp3":["mp3","mpeg"], "wav": ["wav","x-wav","vnd.wav"], "flac":["x-flac", "flac"], }
    supported_content_length = os.environ.get('supported_content_length', 3145728)
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
