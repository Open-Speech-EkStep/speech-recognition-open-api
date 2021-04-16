import requests
import wave
import os


def download_from_url_to_file(file_name, url):
    r = requests.get(url, allow_redirects=True)
    with open(file_name, 'wb') as f:
        f.write(r.content)
    return os.path.join(os.getcwd(), file_name)


def create_wav_file_using_bytes(file_name, audio):
    with wave.open(file_name, 'wb') as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(16000.0)
        file.writeframes(audio)
    return os.path.join(os.getcwd(), file_name)


def convert_audio_to_required_format(file_name):
    pass
