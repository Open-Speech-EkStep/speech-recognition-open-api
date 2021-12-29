import time

from src import log_setup

LOGGER = log_setup.get_logger(__name__)


def monitor(func):
    def wrapped_function(*args, **kwargs):
        start = time.monotonic_ns()
        return_value = func(*args, **kwargs)
        LOGGER.info(
            f'function {func.__name__} took {(time.monotonic_ns() - start) / 1000000} milliseconds with arguments {args}')
        return return_value

    return wrapped_function
