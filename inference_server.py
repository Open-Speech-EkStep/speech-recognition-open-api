from string import punctuation
import uuid
from cairo import Path
from sanic.log import logger
from sanic.response import json
import os, torch
from sanic import  Request, Sanic
from sanic_cors import CORS
from src.lib.inference_lib import get_results, load_model_and_generator

from src.model_item import ModelItem

app = Sanic(__name__)
config = {}
config["upload"] = "/opt/speech_recognition_open_api/uploads"

model_base_path = "/opt/speech_recognition_open_api/deployed_models/"
gpu = True
decoder_type = "kenlm"
cuda = gpu
half = gpu

def create_app():
    """ Function for bootstrapping sanic app. """
    CORS(app)

    # error hanlder
    app.config.FALLBACK_ERROR_FORMAT = "json"
    
    # on server start
    app.before_server_start(load_model)

    # on server end
    app.before_server_stop(unload_model)

    app.go_fast(debug=False, workers=2, host='0.0.0.0', access_log=False,auto_reload=True, port=6666)



@app.route("/upload", methods=['POST'])
def upload_audio(request : Request):
    if not os.path.exists(config["upload"]):
        os.makedirs(config["upload"])
    
    try:
        test_file = request.files.get("audio")
        file_parameters = {
            'body': test_file.body,
            'name': test_file.name,
            'type': test_file.type,
        }

        if str(file_parameters['name']).endswith('.wav'):
            uid = str(uuid.uuid4())
            file_path = f"{config['upload']}/{uid}/{file_parameters['name']}"
            with open(file_path, 'wb') as f:
                f.write(file_parameters['body'])

            logger.info(f'file wrote to disk - {file_path}')
            model_item = request.app.config.MODEL_ITEM
            res = get_transcript(Path(file_path), model_item)

            return json({ "transcription": res, "file_name": file_parameters['name'], "success": True })
        
        return json({ "received": False, "file_name": file_parameters['name'], "success": False, "status": "invalid file uploaded" })
    except Exception as e:
        return json({"error": "bad_request", "log": str(e)}, status=403)



def get_transcript(wav_path : Path, model_item) -> str:
    result = get_results(
        wav_path=wav_path,
        dict_path=model_item.get_dict_file_path(),
        generator=model_item.get_generator(),
        use_cuda=cuda,
        model=model_item.get_model(),
        half=half
    )

    return result

async def load_model(app : Sanic, loop):
    model_config_file_path=model_base_path + 'model_dict.json'
    if os.path.exists(model_config_file_path):
        with open(model_config_file_path, 'r') as f:
            model_config = json.load(f)
    else:
        raise Exception(f'Model configuration file is missing at {model_config_file_path}')
    
    logger.info(f'configuration from model_dict.json is {model_config}')
    model_items = {}
    cuda = cuda
    half = half
    punc_models_dict = {}
    enabled_itn_lang_dict = {}
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

            # setting default model
            app.config.MODEL_ITEM = model_item

            model_items[language_code] = model_item
            logger.info(f"Loaded {language_code} model base_path is {base_path}")
            if lang_config["enablePunctuation"]:
                punc_models_dict[language_code] = punctuation(language_code)
                logger.info(f"Loaded {language_code} model with Punctuation")
            if lang_config["enableITN"]:
                enabled_itn_lang_dict[language_code] = 1
                logger.info(f"Loaded {language_code} model with ITN")


async def unload_model(app, loop):
    pass

def get_gpu_info(gpu):
    logger.info(f"*** GPU is enabled: {gpu} ***")
    if gpu:
        no_gpus = torch.cuda.device_count()
        logger.info(f"*** Total number of gpus allocated are {no_gpus} ***")
        logger.info(f"*** Cuda Version {torch.version.cuda} ***")
        logger.info(f"*** Python process id {os.getpid()} ***")
        logger.info("*** The gpu device info : ***")
        for gpu in range(0, no_gpus):
            logger.info(f"GPU {str(gpu)} - {str(torch.cuda.get_device_name(gpu))}")

if __name__ == '__main__':
    create_app()