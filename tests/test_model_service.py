from path_setter import set_root_folder_path
set_root_folder_path()
from src.model_service import ModelService
import os
import unittest.mock as mock

def mock_load_model_and_generator(model_item, cuda, decoder, half):
    return mock.MagicMock(), mock.MagicMock()
    
def mock_get_results(wav_path,
        dict_path,
        generator,
        use_cuda,
        model,
        half):
    return 'hello'

def mock_monitor():
    pass

def test_transcribe(mocker):
    res = {'status':'OK', 'transcription': 'hello'}

    mocker.patch('src.model_service.load_model_and_generator', mock_load_model_and_generator)
    mocker.patch('src.model_service.get_results', mock_get_results)
    mocker.patch('src.model_service.monitor', mock_monitor)
    os.environ["UTILITIES_FILES_PATH"] = ""

    model_dict_path = 'tests/resources/'
    model = ModelService(model_dict_path, "viterbi", False, False)
    file_name = 'test.wav'
    language = 'hi'
    result = model.transcribe(file_name, language,punctuate=False, itn=False)

    assert result == res


def test_srt(mocker):
    srt_string = '1\n00:00:01,29 --> 00:00:04,88\nHello how are you\n\n'
    res = {'srt': srt_string}

    def mock_get_srt(file, model, generator, dict_file_path,
                           denoiser_path, audio_threshold,
                           language, half):
        return srt_string


    mocker.patch('src.model_service.load_model_and_generator', mock_load_model_and_generator)
    mocker.patch('src.model_service.get_results', mock_get_results)
    mocker.patch('src.model_service.monitor', mock_monitor)
    mocker.patch('src.model_service.get_srt', mock_get_srt)

    os.environ["UTILITIES_FILES_PATH"] = ""

    model_dict_path = 'tests/resources/'
    model = ModelService(model_dict_path, "viterbi", False, False)
    file_name = 'test.wav'
    language = 'hi'
    result = model.get_srt(file_name, language, punctuate=False, itn=False)

    assert result == res



def test_punctuation(mocker):
    text_to_punctuate = "Hello how are you"
    res = ["Hello,  how are you?"]
    class MockPunctuation:
        def __init__(self, lang):
            self.lang = lang

        def punctuate_text(self, text_to_punctuate):
            return res

    mocker.patch('src.model_service.Punctuation', MockPunctuation)
    mocker.patch('src.model_service.load_model_and_generator', mock_load_model_and_generator)
    mocker.patch('src.model_service.get_results', mock_get_results)
    mocker.patch('src.model_service.monitor', mock_monitor)
    os.environ["UTILITIES_FILES_PATH"] = ""

    model_dict_path = 'tests/resources/'

    model = ModelService(model_dict_path, "viterbi", False, False)
    # file_name = 'test.wav'
    language = 'en'
    punctuate = True
    result = model.apply_punctuation(text_to_punctuate, language, punctuate)

    assert result == res[0]


def test_itn(mocker):
    text_to_itn = "Four Hundred Dollars"
    res = ["400 Dollars"]

    def mock_inverse_normalize_text(text_to_itn,language):
        return res

    mocker.patch('src.model_service.load_model_and_generator', mock_load_model_and_generator)
    mocker.patch('src.model_service.get_results', mock_get_results)
    mocker.patch('src.model_service.monitor', mock_monitor)
    os.environ["UTILITIES_FILES_PATH"] = ""

    model_dict_path = 'tests/resources/'
    mocker.patch('src.model_service.inverse_normalize_text', mock_inverse_normalize_text)

    model = ModelService(model_dict_path, "viterbi", False, False)
    # file_name = 'test.wav'
    language = 'en'
    itn = True
    result = model.apply_itn(text_to_itn, language, itn)

    assert result == res[0]

