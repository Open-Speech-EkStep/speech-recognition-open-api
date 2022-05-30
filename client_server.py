from sanic.log import logger
from datetime import datetime
from sanic.response import json
import os
from sanic import  Sanic
from sanic_cors import CORS

app = Sanic(__name__)
config = {}
config["upload"] = "./test/uploads"

BASE_URL = ""

def create_app():
    """ Function for bootstrapping sanic app. """
    CORS(app)

    # error hanlder
    app.config.FALLBACK_ERROR_FORMAT = "json"
    

    app.go_fast(debug=False, workers=2, host='0.0.0.0', access_log=False,auto_reload=True, port=6666)



@app.route("/upload", methods=['POST'])
def upload_audio(request):
    if not os.path.exists(config["upload"]):
        os.makedirs(config["upload"])
    
    try:
        test_file = request.files.get("audio")
        file_parameters = {
            'body': test_file.body,
            'name': test_file.name,
            'type': test_file.type,
        }

        if file_parameters['name'].split('.')[-1] == 'wav':
            file_path = f"{config['upload']}/{file_parameters['name']}"
            with open(file_path, 'wb') as f:
                f.write(file_parameters['body'])

            logger.info(f'file wrote to disk - {file_path}')

            return json({ "received": True, "file_name": file_parameters['name'], "success": True })
        
        return json({ "received": False, "file_name": file_parameters['name'], "success": False, "status": "invalid file uploaded" })
    except Exception as e:
        return json({"error": "bad_request", "log": str(e)}, status=403)



def get_transcript() -> str:
    pass


if __name__ == '__main__':
    create_app()