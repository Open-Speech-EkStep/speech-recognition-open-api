# from inference_module import InferenceService
import itertools
import json
import os

import torch
from inverse_text_normalization.run_predict import inverse_normalize_text
from punctuate.punctuate_text import Punctuation

from src import log_setup, utilities
from src.lib.inference_lib import load_model_and_generator, get_results
from src.model_item import ModelItem
from src.monitoring import monitor
from src.srt.subtitle_generator import get_srt

LOGGER = log_setup.get_logger(__name__)


def get_gpu_info(gpu):
    LOGGER.info(f"*** GPU is enabled: {gpu} ***")
    if gpu:
        no_gpus = torch.cuda.device_count()
        LOGGER.info(f"*** Total number of gpus allocated are {no_gpus} ***")
        LOGGER.info("*** The gpu device info : ***")
        for gpu in range(0, no_gpus):
            LOGGER.info(f"GPU {str(gpu)} - {str(torch.cuda.get_device_name(gpu))}")


class ModelService:

    def __init__(self, model_base_path, decoder_type, cuda, half):
        languages = utilities.get_env_var('languages', ['all'])
        model_config_file_path = model_base_path + 'model_dict.json'
        if os.path.exists(model_config_file_path):
            with open(model_config_file_path, 'r') as f:
                model_config = json.load(f)
        else:
            raise Exception(f'Model configuration file is missing at {model_config_file_path}')
        self.model_items = {}
        self.cuda = cuda
        self.half = half
        self.punc_models_dict = {}
        self.enabled_itn_lang_dict = {}
        self.supported_languages = list(model_config.keys())
        get_gpu_info(self.cuda)
        for language_code, lang_config in model_config.items():
            if language_code in languages or 'all' in languages:
                path_split = lang_config["path"].split("/")
                base_path = model_base_path[:-1] + "/".join(path_split[:-1])
                model_file_name = path_split[-1]
                model_item = ModelItem(base_path, model_file_name, language_code)
                model, generator = load_model_and_generator(model_item, self.cuda, decoder=decoder_type, half=self.half)
                model_item.set_model(model)
                model_item.set_generator(generator)
                self.model_items[language_code] = model_item
                LOGGER.info(f"Loaded {language_code} model base_path is {base_path}")
                if lang_config["enablePunctuation"]:
                    self.punc_models_dict[language_code] = Punctuation(language_code)
                    LOGGER.info(f"Loaded {language_code} model with Punctuation")
                if lang_config["enableITN"]:
                    self.enabled_itn_lang_dict[language_code] = 1
                    LOGGER.info(f"Loaded {language_code} model with ITN")

    @monitor
    def transcribe(self, file_name, language, punctuate, itn):
        model_item = self.model_items[language]
        response = get_results(
            wav_path=file_name,
            dict_path=model_item.get_dict_file_path(),
            generator=model_item.get_generator(),
            use_cuda=self.cuda,
            model=model_item.get_model(),
            half=self.half
        )
        LOGGER.debug("The model transcript is: %s", response)
        punctuated_text = self.apply_punctuation(response, language, punctuate)
        itn_text = self.apply_itn(punctuated_text, language, itn)
        LOGGER.debug("The model transcript after punctuation and itn: %s", itn_text)
        return {
            'transcription': itn_text,
            'status': 'OK'
        }

    @monitor
    def get_srt(self, file_name, language, punctuate, itn):
        model_item = self.model_items[language]
        model = model_item.get_model()
        generator = model_item.get_generator()
        dict_file_path = model_item.get_dict_file_path()
        result = {}
        response = get_srt(file_name, model, generator, dict_file_path,
                           os.path.dirname(__file__) + '/denoiser', audio_threshold=15,
                           language=language, half=self.half)
        response = [i.replace('\n', ' ') for i in list(itertools.chain(*response)) if type(i) != bool]
        result['srt'] = ''.join(response)
        result['srt'] = self.apply_punctuation(result['srt'], language, punctuate)
        result['srt'] = self.apply_itn(result['srt'], language, itn)
        LOGGER.info("*** The model SRT is *** ", result['srt'])
        return result

    @monitor
    def apply_punctuation(self, text_to_punctuate, language, punctuate):
        result = text_to_punctuate
        if punctuate and result not in ('', 'null', 'Null'):
            punc_model_obj = self.punc_models_dict.get(language, None)
            if punc_model_obj != None:
                result = punc_model_obj.punctuate_text([text_to_punctuate])[0]
        return result

    @monitor
    def apply_itn(self, text_to_itn, language, itn):
        result = text_to_itn
        if itn and result not in ('', 'null', 'Null'):
            enabled_itn = self.enabled_itn_lang_dict.get(language, None)
            if enabled_itn != None:
                result = inverse_normalize_text([text_to_itn], language)[0]
        return result
