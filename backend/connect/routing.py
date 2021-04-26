#print('__FILE__: ', __file__)

#
import logging

import typing

import time
import inspect

import re
import ujson
import orjson

from .message import Message, RES_Exception, RES_ERROR

from .function import function, function_
from .profile import profile

####
logger = logging.getLogger(__name__)

_http_post_dict = dict()
_websocket_dict = dict()

'''
def method(func: typing.Callable) -> typing.Callable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__
    key = func.__name__
    logger.info("->> method -> '" + key + "' from " + func.__module__)

    _msg_methods[key] = func
    return func
'''

def post(func: typing.Callable) -> typing.Callable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__

    @function
    async def decorator(*args, **kwargs) -> typing.Callable:
        logger.info('-->> ' + func.__module__)

        start_time = time.perf_counter()

        try:
            response = await func(*args, **kwargs)

        except Exception as e:
            logger.exception(e)

            req = Message(RES_Exception)
            req.T.message = str(type(e).__name__ + " " + str(e))

            response = req.dict

        finally:
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            logger.info('<<-- ' + func.__module__ + '.' + func.__name__ + ': ELAPSED TIME: ' + str(elapsed_time))

            return response


    key = func.__name__
    logger.info('<<- ' + key)

    _http_post_dict[key] = decorator

    return decorator

def websocket(func: typing.Callable) -> typing.Callable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__

    @function
    async def decorator(*args, **kwargs) -> typing.Callable:
        logger.info('-->> ' + func.__module__ + '.' + key)

        response = {}
        start_time = time.perf_counter()

        try:
            response = await func(*args, **kwargs)

        except Exception as e:
            logger.exception(e)

            req = Message(RES_Exception)
            req.T.message = str(type(e).__name__ + " " + str(e))

            response = req.dict

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        logger.info('<<-- ' + func.__module__ + '.' + func.__name__ + ': ELAPSED TIME: ' + str(elapsed_time))

        return response


    key = func.__name__
    #logger.info("--->> METHOD: '" + func.__module__ + '.' + key + "' from " + func.__module__)
    logger.info('->> register websocket - ' + func.__module__ + '.' + key)

    _websocket_dict[key] = decorator

    return decorator

'''
def id_(id: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        print(">> pid: '" + id + "' from " + func.__module__)

        api_dict[id] = func

        return func

    return decorator
'''

@function
async def run_http_post(body: typing.Any) -> typing.Any:
    #response = {}

    try:
        pid = body['pid']
        args = body['args'] if 'args' in body else {}
        kwargs = body['kwargs'] if 'kwargs' in body else {}
        response = await _http_post_dict[pid](*args, **kwargs)

        #args = body['args'] if 'args' in body else {}
        #kwargs = body['kwargs'] if 'kwargs' in body else args
        #result = await _method_dict[pid](kwargs)
    
    except Exception as e:
        logger.exception(e)

        req = Message(RES_Exception)
        req.T.message = str(type(e).__name__ + " " + str(e))

        response = req.dict

    finally:
        return response


@function
async def run_websocket(body: typing.Any) -> typing.Any:
    response = {}

    try:
        pid = body['pid']
        args = body['args'] if 'args' in body else {}
        kwargs = body['kwargs'] if 'kwargs' in body else {}
        response = await _websocket_dict[pid](*args, **kwargs)

        #args = body['args'] if 'args' in body else {}
        #kwargs = body['kwargs'] if 'kwargs' in body else args
        #result = await _method_dict[pid](kwargs)
    
    except Exception as e:
        logger.exception(e)

        req = Message(RES_Exception)
        req.T.message = str(type(e).__name__ + " " + str(e))

        response = req.dict

    finally:
        return result
