import os
import responses

from utilities import download_from_url_to_file, create_wav_file_using_bytes, write_to_file, get_current_time_in_millis


@responses.activate
def test_download_from_url_to_file():
    url = 'http://example.org/test.wav'
    file_name = 'test_download_from_url_to_file.wav'
    with open('changed.wav', 'rb') as file:
        responses.add(responses.GET, url,
                      body=file.read(), status=200,
                      content_type='audio/wav',
                      adding_headers={'Transfer-Encoding': 'chunked'})
        file_path = download_from_url_to_file(file_name, url)
        assert os.path.exists(file_path)
        os.remove(file_path)
        assert not os.path.exists(file_path)
        assert file_path == os.path.join(os.getcwd(), file_name)


def test_create_wav_file_using_bytes():
    file_name = 'create_wav_file_using_bytes.wav'
    audio_bytes = b'test_wav_bytes.wav'
    file_path = create_wav_file_using_bytes(file_name, audio_bytes)
    assert os.path.exists(file_path)
    os.remove(file_path)
    assert not os.path.exists(file_path)
    assert file_path == os.path.join(os.getcwd(), file_name)


def test_write_to_file():
    file_name = 'test_write_to_file.wav'
    audio_bytes = b'test_write_to_file.wav'
    file_path = write_to_file(file_name, audio_bytes)
    assert os.path.exists(file_path)
    os.remove(file_path)
    assert not os.path.exists(file_path)
    assert file_path == os.path.join(os.getcwd(), file_name)


def test_get_current_time_in_millis(mocker):
    def time_mock():
        return 123

    mocker.patch('utilities.time.time', time_mock)

    time = get_current_time_in_millis()

    assert time == 123000
