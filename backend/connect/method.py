#print('__FILE__: ', __file__)

#
import logging
import typing

import time
import inspect

import ujson

####
logger = logging.getLogger(__name__)

_method_dict = dict()

'''
def method(func: typing.Callable) -> typing.Callable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__
    key = func.__name__
    logger.info("->> method -> '" + key + "' from " + func.__module__)

    _msg_methods[key] = func
    return func
'''

def method(func: typing.Callable) -> typing.Callable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__

    async def decorator(*args, **kwargs) -> typing.Callable:
        start_time = time.perf_counter()

        logger.info('async def ' + func.__module__ + '.' + key)

        result = await func(*args, **kwargs)

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info('async def ' + func.__module__ + '.' + func.__name__ + ': ELAPSED TIME: ' + str(elapsed_time))

        return result


    key = func.__name__
    #logger.info("--->> METHOD: '" + func.__module__ + '.' + key + "' from " + func.__module__)
    logger.info('->> register method - ' + func.__module__ + '.' + key)

    _method_dict[key] = decorator

    return decorator

'''
def id_(id: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        print(">> pid: '" + id + "' from " + func.__module__)

        api_dict[id] = func

        return func

    return decorator
'''

async def run_method(body: typing.Any) -> typing.Any:
    result = {}

    try:
        method = body['method']
        args = body['args'] if 'args' in body else {}
        kwargs = body['kwargs'] if 'kwargs' in body else {}        
        result = await _method_dict[method](*args, **kwargs)

        #args = body['args'] if 'args' in body else {}
        #kwargs = body['kwargs'] if 'kwargs' in body else args
        #result = await _method_dict[method](kwargs)
    
    except Exception as e:
        text = str(type(e).__name__ + " " + str(e))
        result['method'] = 'run_method()'
        result['kwargs'] = text

        logger.exception("Unhandled exception: " + text)
        #raise

    finally:
        return result
