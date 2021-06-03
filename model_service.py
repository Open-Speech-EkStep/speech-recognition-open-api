from inference_module import InferenceService
from punctuate.punctuate_text import Punctuation
# from inverse_text_normalization.run_predict import run_itn
import os


class ModelService:

    def __init__(self, model_dict_path):
        self.inference = InferenceService(model_dict_path)
        self.punc_models_dict = {'hi': Punctuation('hi')}

    def transcribe(self, file_name, language, punctuate=True):
        result = self.inference.get_inference(file_name, language)
        result['transcription'] = self.apply_puncuation(result['transcription'], language, punctuate)
        return result

    def get_srt(self, file_name, language):
        result = self.inference.get_srt(file_name, language, os.path.dirname(__file__) + '/denoiser')
        return result

    def apply_puncuation(self, text_to_punctuate, language, punctuate=True):
        result = text_to_punctuate
        if punctuate:
            punc_model_obj = self.punc_models_dict.get(language, 'hi')
            result = punc_model_obj.punctuate_text(text_to_punctuate)
        return result
