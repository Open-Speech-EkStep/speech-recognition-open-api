import json
import os
import wave
from pathlib import Path

import grpc
import requests
import torch

from src import log_setup
from src.model_service import ModelService
from src.monitoring import monitor
from src.speech_recognition_service_handler import handle_request
from stub import speech_recognition_open_api_pb2_grpc
from stub.speech_recognition_open_api_pb2 import SpeechRecognitionResult, Language, RecognitionConfig, Response, \
    PunctuateResponse
from src.utilities import download_from_url_to_file, create_wav_file_using_bytes, get_current_time_in_millis, \
    get_env_var, create_temp_dir, delete_directory

LOGGER = log_setup.get_logger(__name__)


# add error message field to status
# handle grpc thrown error from server
# move default field of Model field to 0 from 3
class SpeechRecognizer(speech_recognition_open_api_pb2_grpc.SpeechRecognizerServicer):

    def __init__(self):
        LOGGER.info('Initializing realtime and batch inference service')
        self.MODEL_BASE_PATH = get_env_var('models_base_path')
        self.BASE_PATH = get_env_var('base_path')

        gpu = get_env_var('gpu', 'false')
        if gpu == 'true' or gpu == 'True':
            gpu = True
        else:
            gpu = False
        LOGGER.info(f'User has provided gpu as {gpu}')

        gpu_present = torch.cuda.is_available()
        LOGGER.info(f'GPU available on machine {gpu_present}')
        gpu = gpu & gpu_present

        LOGGER.info(f'Loading models from {self.MODEL_BASE_PATH} with gpu value: {gpu}')
        self.model_service = ModelService(self.MODEL_BASE_PATH, 'kenlm', gpu, gpu)
        self.count = 0
        self.file_count = 0
        self.client_buffers = {}
        self.client_transcription = {}
        LOGGER.info('Models Loaded Successfully')
        Path(self.BASE_PATH + 'Startup.done').touch()

    # Batch API request handler
    @monitor
    def recognize(self, request, context):
        try:
            handle_request(request, self.model_service.supported_languages)
        except NotImplementedError as e:
            LOGGER.exception('Validation failed %s', e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return SpeechRecognitionResult(status='ERROR', status_text=str(e))
        except ValueError as e:
            LOGGER.exception('Value error %s', e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return SpeechRecognitionResult(status='ERROR', status_text=str(e))

        punctuate = request.config.punctuation
        itn = request.config.enableInverseTextNormalization
        language = Language.LanguageCode.Name(request.config.language.sourceLanguage)
        audio_format = RecognitionConfig.AudioFormat.Name(request.config.audioFormat)
        out_format = RecognitionConfig.TranscriptionFormatEnum.Name(request.config.transcriptionFormat.value)
        model_output_list = []
        LOGGER.info(
            f"The request parameters are (language:{language},output_format:{out_format},audio_format:{audio_format},punctuation :{punctuate},enableInverseTextNormalization:{itn})")
        for audio_obj in request.audio:
            # create temp location for audio processing
            temp_location = create_temp_dir()
            LOGGER.debug(f'created temp directory {temp_location}')
            audio_path = Path(temp_location + '/audio_input_{}.{}'.format(str(get_current_time_in_millis()),
                                                                    audio_format.lower()))
            try:
                if len(audio_obj.audioUri) != 0:
                    audio_path = download_from_url_to_file(audio_path, audio_obj.audioUri, audio_format)
                elif len(audio_obj.audioContent) != 0:
                    audio_path = create_wav_file_using_bytes(audio_path, audio_obj.audioContent)
                if out_format == 'srt':
                    response = self.model_service.get_srt(audio_path, language, punctuate, itn)
                    output = SpeechRecognitionResult.Output(source=response['srt'])
                    model_output_list.append(output)

                else:
                    response = self.model_service.transcribe(audio_path, language, punctuate, itn)
                    output = SpeechRecognitionResult.Output(source=response['transcription'])
                    model_output_list.append(output)

            except ValueError as e:
                LOGGER.exception('Recognize failed %s', e)
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return SpeechRecognitionResult(status='ERROR',
                                               status_text=str(e))

            except requests.exceptions.RequestException as e:
                LOGGER.exception('Request exception %s', e)
                context.set_details("Audio file url is incorrect or can't be accessed")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return SpeechRecognitionResult(status='ERROR',
                                               status_text="Audio file url is incorrect or can't be accessed")
            except Exception as e:
                LOGGER.exception('Exception %s', e)
                context.set_details("An unknown error has occurred.Please try again.")
                context.set_code(grpc.StatusCode.UNKNOWN)
                return SpeechRecognitionResult(status='ERROR',
                                               status_text="An unknown error has occurred.Please try again.")
            finally:
                # cleanup temp location
                LOGGER.debug(f'removing directory {temp_location}')
                delete_directory(temp_location)

        result = SpeechRecognitionResult(status='SUCCESS', output=model_output_list)
        return result

    # Streaming handler
    def recognize_audio(self, request_iterator, context):
        for data in request_iterator:
            self.count += 1
            LOGGER.debug("Request received for user %s language: %s data.isEnd: %s", data.user, data.language,
                         data.isEnd)
            LOGGER.info(" Total Connected Users: %s ", len(self.client_buffers))
            if data.isEnd:
                self.disconnect(data.user)
                result = {}
                result["id"] = self.count
                result["success"] = True
                yield Response(transcription=json.dumps(result), user=data.user, action="terminate",
                               language=data.language)
            else:
                buffer, append_result, local_file_name = self.preprocess(data)
                if append_result and buffer is not None:
                    transcription = self.transcribe(buffer, str(self.count), data, append_result, local_file_name)
                    yield Response(transcription=transcription, user=data.user, action=str(append_result),
                                   language=data.language)

    @monitor
    def punctuate(self, request, context):
        response = self.model_service.apply_punctuation(request.text, request.language, True)
        response = self.model_service.apply_itn(response, request.language, request.enabledItn)
        return PunctuateResponse(text=response, language=request.language)

    def disconnect(self, user):
        self.clear_states(user)
        LOGGER.info("Disconnecting user %s", str(user))

    @monitor
    def transcribe(self, buffer, count, data, append_result, local_file_name):
        index = data.user + count
        user = data.user
        temp_location = create_temp_dir()
        LOGGER.debug(f'created temp directory {temp_location}')

        try:
            input_audio_file = self.write_wave_to_file(temp_location + "/" + index + ".wav", buffer)
            result = self.model_service.transcribe(Path(input_audio_file), data.language, False, False)
            if user not in self.client_transcription:
                self.client_transcription[user] = ""
            transcription = (self.client_transcription[user] + " " + result['transcription']).lstrip()
            result['transcription'] = transcription
            LOGGER.debug("transcription for user %s language: %s transcription: %s", user, data.language, transcription)
            if append_result:
                self.client_transcription[user] = transcription
                if local_file_name is not None:
                    with open(local_file_name.replace(".wav", ".txt"), 'w') as local_file:
                        local_file.write(result['transcription'])
            result["id"] = index
            LOGGER.debug("Responded for user %s language: %s transcription: %s and result %s", user, data.language,
                         transcription, result)

            if result['status'] != "OK":
                result["success"] = False
            else:
                result["success"] = True
        except Exception as e:
            LOGGER.exception('Error in realtime streaming %s', e)
            result["success"] = False
        finally:
            # cleanup temp location
            LOGGER.debug(f'removing directory {temp_location}')
            delete_directory(temp_location)

        return json.dumps(result)

    def write_wave_to_file(self, file_name, audio):
        with wave.open(file_name, 'wb') as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(16000.0)
            file.writeframes(audio)
        return os.path.join(os.getcwd(), file_name)

    def clear_states(self, user):
        self.clear_buffers(user)
        self.clear_transcriptions(user)

    def clear_buffers(self, user):
        if user in self.client_buffers:
            del self.client_buffers[user]

    def clear_transcriptions(self, user):
        if user in self.client_transcription:
            del self.client_transcription[user]

    def preprocess(self, data):
        append_result = False
        if data.audio is not None and len(data.audio) > 0:
            LOGGER.debug("Audio length: %s, speaking: %s", len(data.audio), data.speaking)
            if data.user in self.client_buffers:
                self.client_buffers[data.user] += data.audio
            else:
                self.client_buffers[data.user] = data.audio

        buffer = self.client_buffers[data.user] if data.user in self.client_buffers else None
        if not data.speaking:
            self.clear_buffers(data.user)
            append_result = True
        LOGGER.debug("Buffer length is %s for user %s language: %s isSpeaking: %s",
                     len(buffer) if buffer is not None else 0, data.user, data.language, data.speaking)
        return buffer, append_result, None
