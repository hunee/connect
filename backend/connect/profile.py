import logging
import typing

import time
import inspect

logger = logging.getLogger(__name__)


def profile(func: typing.Callable) -> typing.Callable:
    async def decorator(*args, **kwargs) -> typing.Callable:
        logger.info('-->> ' + func.__module__ + ' - ' + func.__name__)
        
        start_time = time.perf_counter()

        result = await func(*args, **kwargs)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info('<<-- ' + func.__module__ + ' - ' + func.__name__ + ': ELAPSED TIME: ' + str(elapsed_time))

        return result

    return decorator
