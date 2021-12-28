import logging
import os
import sys
import socket
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOGS_MODEL_BASE_PATH = os.environ.get('model_logs_base_path', '')
LOG_FILE = f"inference_" + socket.gethostname() + ".log"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    if not os.path.exists(LOGS_MODEL_BASE_PATH):
        os.makedirs(LOGS_MODEL_BASE_PATH)

    log_file = LOGS_MODEL_BASE_PATH + LOG_FILE
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=30)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
