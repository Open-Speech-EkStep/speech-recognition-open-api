import json
import os
from pathlib import Path

import torch

from src import log_setup
from src.lib.inference_lib import load_model_and_generator, get_results
from src.model_item import ModelItem

LOGGER = log_setup.get_logger(__name__)

model_base_path = "/opt/speech_recognition_open_api/deployed_models/"
gpu = True

LOGGER.info('Initializing realtime and batch inference service')

def get_gpu_info(gpu):
    LOGGER.info(f"*** GPU is enabled: {gpu} ***")
    if gpu:
        no_gpus = torch.cuda.device_count()
        LOGGER.info(f"*** Total number of gpus allocated are {no_gpus} ***")
        LOGGER.info(f"*** Cuda Version {torch.version.cuda} ***")
        LOGGER.info(f"*** Python process id {os.getpid()} ***")
        LOGGER.info("*** The gpu device info : ***")
        for gpu in range(0, no_gpus):
            LOGGER.info(f"GPU {str(gpu)} - {str(torch.cuda.get_device_name(gpu))}")

LOGGER.info('Models Loaded Successfully')

decoder_type = "kenlm"
cuda = gpu
half = gpu

model_config_file_path=model_base_path + 'model_dict.json'
if os.path.exists(model_config_file_path):
    with open(model_config_file_path, 'r') as f:
        model_config = json.load(f)
else:
    raise Exception(f'Model configuration file is missing at {model_config_file_path}')

LOGGER.info(f'configuration from model_dict.json is {model_config}')

model_items = {}
cuda = cuda
half = half
punc_models_dict = {}
enabled_itn_lang_dict = {}
supported_languages = list(model_config.keys())
denoiser_path = os.environ.get('UTILITIES_FILES_PATH') + 'denoiser'
get_gpu_info(cuda)

for language_code, lang_config in model_config.items():
    if language_code in ['en']:
        path_split = lang_config["path"].split("/")
        base_path = model_base_path[:-1] + "/".join(path_split[:-1])
        model_file_name = path_split[-1]
        model_item = ModelItem(base_path, model_file_name, language_code)
        model, generator = load_model_and_generator(model_item, cuda, decoder=decoder_type, half=half)
        model.eval()
        model_item.set_model(model)
        model_item.set_generator(generator)
        model_items[language_code] = model_item
        LOGGER.info(f"Loaded {language_code} model base_path is {base_path}")
        if lang_config["enablePunctuation"]:
            punc_models_dict[language_code] = Punctuation(language_code)
            LOGGER.info(f"Loaded {language_code} model with Punctuation")
        if lang_config["enableITN"]:
            enabled_itn_lang_dict[language_code] = 1
            LOGGER.info(f"Loaded {language_code} model with ITN")
    

    response = get_results(
    wav_path=Path("/opt/speech_recognition_open_api/nt-scripts/audio_in.wav"),
    dict_path=model_item.get_dict_file_path(),
    generator=model_item.get_generator(),
    use_cuda=cuda,
    model=model_item.get_model(),
    half=half
)

response = get_results(
    wav_path=Path("/opt/speech_recognition_open_api/nt-scripts/audio_in.wav"),
    dict_path=model_item.get_dict_file_path(),
    generator=model_item.get_generator(),
    use_cuda=cuda,
    model=model_item.get_model(),
    half=half
)

print(response)