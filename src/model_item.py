class ModelItem:

    def __init__(self, base_path, model_file_name, language_code):
        self.model = None
        self.punctuation_model = None
        self.generator = None
        self.base_path = base_path
        self.language_code = language_code
        self.model_file_name = model_file_name
        self.lexicon_file_name = 'lexicon.lst'
        self.language_model_name = 'lm.binary'
        self.dict_file_name = 'dict.ltr.txt'
        self.punctuation_and_itn_enabled = False

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    def get_generator(self):
        return self.generator

    def set_generator(self, generator):
        self.generator = generator

    def get_model_path(self):
        return self.base_path + "/" + self.model_file_name

    def get_lexicon_path(self):
        return self.base_path + "/" + self.lexicon_file_name

    def get_language_model_path(self):
        return self.base_path + "/" + self.language_model_name

    def get_dict_file_path(self):
        return self.base_path + "/" + self.dict_file_name

    def get_puncutation_model(self):
        return self.punctuation_model

    def set_punctuation_model(self, punctuation_model):
        self.punctuation_model = punctuation_model

    def get_language_code(self):
        return self.language_code

    def is_punctuation_and_itn_enabled(self):
        return self.punctuation_and_itn_enabled

    def set_is_punctuation_and_itn_enabled(self, value):
        self.punctuation_and_itn_enabled = value
