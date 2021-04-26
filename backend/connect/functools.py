#print('__FILE__: ', __file__)

"""@package docstring
Documentation for this module.
 
More details.
"""

import logging
import typing

import time
import inspect

logger = logging.getLogger(__name__)


def function_async(func: typing.Callable) -> typing.Callable:
    """Documentation for a function.
 
    More details.
    """

    async def decorator(*args, **kwargs) -> typing.Callable:
        """Documentation for a function.
    
        More details.
        """

        logger.info('>>> async def ' + func.__module__ + '.' + func.__name__)

        return await func(*args, **kwargs)

    return decorator


###
def function(func: typing.Callable) -> typing.Callable:
    """Documentation for a function.

    More details.
    """

    def decorator(*args, **kwargs) -> typing.Callable:
        """Documentation for a function.

        More details.
        """

        logger.info('>>> def ' + func.__module__ + '.' + func.__name__)

        return func(*args, **kwargs)

    return decorator


###
def profile(func: typing.Callable) -> typing.Callable:
    """Documentation for a function.

    More details.
    """

    async def decorator(*args, **kwargs) -> typing.Callable:
        """Documentation for a function.

        More details.
        """

        logger.info('>>> def ' + func.__module__ + '.' + func.__name__)
        
        start_time = time.perf_counter()

        result = await func(*args, **kwargs)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info('<<< def ' + func.__module__ + '.' + func.__name__ + ' -: ELAPSED TIME: ' + str(elapsed_time))

        return result

    return decorator


###
class Singleton(type):
    """Documentation for a class.
 
    More details.
    """

    _instances = {}

    def __init__(self):
        """The constructor."""
        pass

    def __call__(cls, *args, **kwargs):
        """Documentation for a method."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        #else:  # 매번 __init__ 호출하고 싶으면
        #    cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

