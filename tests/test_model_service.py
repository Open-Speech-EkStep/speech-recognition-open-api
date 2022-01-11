from src.model_service import ModelService


def test_transcribe(mocker):
    res = {'transcription': 'hello'}

    class MockInference:
        def __init__(self, model_dict):
            self.model_dict = model_dict

        def get_inference(self, file_name, language):
            return res

    mocker.patch('model_service.InferenceService', MockInference)
    model_dict_path = 'model_dict.json'
    model = ModelService(model_dict_path)
    file_name = 'test.wav'
    language = 'hi'
    result = model.transcribe(file_name, language,punctuate=False, itn=False)

    assert result == res


def test_srt(mocker):
    res = {'srt': '1\n00:00:01,29 --> 00:00:04,88\nHello how are you\n\n'}

    class MockInference:
        def __init__(self, model_dict):
            self.model_dict = model_dict

        denoiser_path = "/denoiser"

        def get_srt(self, file_name, language, denoiser_path):
            return res

    mocker.patch('model_service.InferenceService', MockInference)
    model_dict_path = 'model_dict.json'
    model = ModelService(model_dict_path)
    file_name = 'test.wav'
    language = 'en-IN'
    result = model.get_srt(file_name, language,punctuate=False, itn=False)

    assert result == res



def test_punctuation(mocker):
    text_to_punctuate = "Hello how are you"
    res = ["Hello,  how are you?"]
    class MockPunctuation:
        def __init__(self, lang):
            self.lang = lang

        def punctuate_text(self, text_to_punctuate):
            return res

    class MockInference:
        def __init__(self, model_dict):
            self.model_dict = model_dict

        def get_inference(self, file_name, language):
            return res

    mocker.patch('model_service.InferenceService', MockInference)
    mocker.patch('model_service.Punctuation', MockPunctuation)
    
    model_dict_path = 'model_dict.json'
    model = ModelService(model_dict_path)
    # file_name = 'test.wav'
    language = 'en'
    punctuate = True
    result = model.apply_punctuation(text_to_punctuate, language, punctuate)

    assert result == res[0]


def test_itn(mocker):
    text_to_itn = "Four Hundred Dollars"
    res = ["400 Dollars"]


    class MockInference:
        def __init__(self, model_dict):
            self.model_dict = model_dict

        def get_inference(self, file_name, language):
            return res
    def mock_inverse_normalize_text(text_to_itn,language):
        return res

    mocker.patch('model_service.InferenceService', MockInference)
    mocker.patch('model_service.inverse_normalize_text', mock_inverse_normalize_text)

    model_dict_path = 'model_dict.json'
    model = ModelService(model_dict_path)
    # file_name = 'test.wav'
    language = 'en'
    itn = True
    result = model.apply_itn(text_to_itn, language, itn)

    assert result == res[0]

