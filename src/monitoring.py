import time

from src import log_setup

LOGGER = log_setup.get_logger('model-inference-service')


def monitor(func):
    def wrapped_function(*args, **kwargs):
        start = time.monotonic_ns()
        print('Start of time', args, kwargs)
        return_value = func(*args, **kwargs)
        LOGGER.info(f'function {func.__name__} took {(time.monotonic_ns() - start) / 1000000} milliseconds')
        return return_value

    return wrapped_function
