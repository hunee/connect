import logging
import typing

import time
import inspect

logger = logging.getLogger(__name__)

def function(func: typing.Callable) -> typing.Callable:
    async def decorator(*args, **kwargs) -> typing.Callable:
        logger.info('->> async def ' + func.__module__ + '.' + func.__name__)

        return await func(*args, **kwargs)

    return decorator


def function_(func: typing.Callable) -> typing.Callable:
    def decorator(*args, **kwargs) -> typing.Callable:
        logger.info('->> def ' + func.__module__ + '.' + func.__name__)

        return func(*args, **kwargs)

    return decorator

