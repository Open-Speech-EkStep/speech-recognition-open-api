from inference_module import InferenceService
from punctuate.punctuate_text import Punctuation
from inverse_text_normalization.run_predict import inverse_normalize_text
import os


class ModelService:

    def __init__(self, model_dict_path):
        self.inference = InferenceService(model_dict_path)
        self.punc_models_dict = {'hi': Punctuation('hi'), 'en': Punctuation('en')}
        self.enabled_itn_lang_dict = {'hi': 1, 'en': 1}

    def transcribe(self, file_name, language, punctuate, itn):
        result = self.inference.get_inference(file_name, language)
        result['transcription'] = self.apply_punctuation(result['transcription'], language, punctuate)
        result['transcription'] = self.apply_itn(result['transcription'], language, itn)
        return result

    def get_srt(self, file_name, language, punctuate, itn):
        result = self.inference.get_srt(file_name, language, os.path.dirname(__file__) + '/denoiser')
        result['srt'] = self.apply_punctuation(result['srt'], language, punctuate)
        result['srt'] = self.apply_itn(result['srt'], language, itn)
        return result

    def apply_punctuation(self, text_to_punctuate, language, punctuate):
        result = text_to_punctuate
        if punctuate:
            punc_model_obj = self.punc_models_dict.get(language, None)
            if punc_model_obj != None:
                result = punc_model_obj.punctuate_text([text_to_punctuate])[0]
        return result

    def apply_itn(self, text_to_itn, language, itn):
        result = text_to_itn
        if itn:
            enabled_itn = self.punc_models_dict.get(language, None)
            if enabled_itn != None:
                result = inverse_normalize_text([text_to_itn], language)[0]
        return result
