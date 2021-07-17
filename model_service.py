# from inference_module import InferenceService
import itertools
import json
import os

from punctuate.punctuate_text import Punctuation
from srt.subtitle_generator import get_srt

# from inverse_text_normalization.run_predict import inverse_normalize_text
from lib.inference_lib import load_model_and_generator, get_results
from model_item import ModelItem


class ModelService:

    def __init__(self, model_config_path, decoder_type, cuda, half):
        languages = os.environ.get('languages', ['all'])
        with open(model_config_path, 'r') as f:
            model_config = json.load(f)
        self.model_items = {}
        self.cuda = cuda
        self.half = half
        for language_code, path in model_config.items():
            if language_code in languages or 'all' in languages:
                path_split = path.split("/")
                base_path = "/".join(path_split[:-1])
                model_file_name = path_split[-1]
                model_item = ModelItem(base_path, model_file_name, language_code)

                model, generator = load_model_and_generator(model_item, self.cuda, decoder=decoder_type, half=self.half)
                model_item.set_model(model)
                model_item.set_generator(generator)
                self.model_items[language_code] = model_item
                print(f"Loaded {language_code} model")
        self.punc_models_dict = {'hi': Punctuation('hi'), 'en': Punctuation('en')}
        self.enabled_itn_lang_dict = {'hi': 1, 'en': 1}

    def transcribe(self, file_name, language, punctuate, itn):
        model_item = self.model_items[language]
        result = {}
        response = get_results(
            wav_path=file_name,
            dict_path=model_item.get_dict_file_path(),
            generator=model_item.get_generator(),
            use_cuda=self.cuda,
            model=model_item.get_model(),
            half=self.half
        )
        # result = self.inference.get_inference(file_name, language)
        result['transcription'] = response
        print("Before Punctuation**** ", result['transcription'])
        result['transcription'] = self.apply_punctuation(result['transcription'], language, punctuate)
        # result['transcription'] = self.apply_itn(result['transcription'], language, itn)
        print("After Punctuation**** ", result['transcription'])
        return result

    def get_srt(self, file_name, language, punctuate, itn):
        model_item = self.model_items[language]
        model = model_item.get_model()
        generator = model_item.get_generator()
        dict_file_path = model_item.get_dict_file_path()
        result = {}
        response = get_srt(file_name, model, generator, dict_file_path,
                           os.path.dirname(__file__) + '/denoiser', audio_threshold=15,
                           language=language, half=self.half)
        # result = self.inference.get_srt(file_name, language, os.path.dirname(__file__) + '/denoiser')
        response = [i.replace('\n', ' ') for i in list(itertools.chain(*response)) if type(i) != bool]
        result['srt'] = ''.join(response)
        print("Before Punctuation**** ", result['srt'])
        result['srt'] = self.apply_punctuation(result['srt'], language, punctuate)
        # result['srt'] = self.apply_itn(result['srt'], language, itn)
        print("After Punctuation**** ", result['srt'])
        return result

    def apply_punctuation(self, text_to_punctuate, language, punctuate):
        result = text_to_punctuate
        if punctuate:
            punc_model_obj = self.punc_models_dict.get(language, None)
            if punc_model_obj != None:
                result = punc_model_obj.punctuate_text([text_to_punctuate])[0]
        return result

    # def apply_itn(self, text_to_itn, language, itn):
    #     result = text_to_itn
    #     if itn:
    #         enabled_itn = self.enabled_itn_lang_dict.get(language, None)
    #         if enabled_itn != None:
    #             result = inverse_normalize_text([text_to_itn], language)[0]
    #     return result
