import logging
import os
import socket
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

_FORMATTER = logging.Formatter(
    "%(asctime)s — [%(threadName)s] - %(name)s -  %(filename)s.%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s")
LOGS_MODEL_BASE_PATH = Path(os.environ.get('model_logs_base_path', os.getcwd()))
LOG_FILE = f"inference_" + socket.gethostname() + ".log"

_FILE_LOGGER_HANDLER = None
_CONSOLE_LOGGER_HANDLER = None
_LOGGING_DEBUG = os.environ.get('log_level', 'DEBUG')


def get_console_handler():
    global _CONSOLE_LOGGER_HANDLER
    if _CONSOLE_LOGGER_HANDLER is None:
        _CONSOLE_LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
        _CONSOLE_LOGGER_HANDLER.setFormatter(_FORMATTER)

    return _CONSOLE_LOGGER_HANDLER


def get_file_handler():
    global _FILE_LOGGER_HANDLER
    if _FILE_LOGGER_HANDLER is None:
        if not os.path.exists(LOGS_MODEL_BASE_PATH):
            os.makedirs(LOGS_MODEL_BASE_PATH)
        _FILE_LOGGER_HANDLER = TimedRotatingFileHandler(LOGS_MODEL_BASE_PATH / LOG_FILE,
                                                        when='midnight',
                                                        backupCount=30)
        _FILE_LOGGER_HANDLER.setFormatter(_FORMATTER)

    return _FILE_LOGGER_HANDLER


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(_LOGGING_DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
