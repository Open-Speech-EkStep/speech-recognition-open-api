from inference_module import InferenceService

class ModelService:

    def __init__(self, model_dict_path):
        self.inference = InferenceService(model_dict_path)
    
    def transcribe(self, file_name, language):
        result = self.inference.get_inference(file_name,language)
        return result