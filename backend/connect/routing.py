#print('__FILE__: ', __file__)

#
import typing

from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    Union,
)

from .types import (
    ASGIApp, #
    Receive,
    Scope,
    Send,
    DecoratedCallable, # fastapi
)


import logging
import traceback
import sys

import ujson


logger = logging.getLogger(__name__)

api_dict = dict()

def method():
    pass

def property():
    pass

def api(func: DecoratedCallable) -> DecoratedCallable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__
    key = func.__name__
    logger.info("Registering API -> '" + key + "' from " + func.__module__)

    api_dict[key] = func
    return func

'''
def api_(id: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        print(">> pid: '" + id + "' from " + func.__module__)

        api_dict[id] = func

        return func

    return decorator
'''

#curl -d '{"api":"del_user", "args":{"type":"a", "text":"b", "trash":"true"}}' -H "Content-Type: application/json" -X POST http://localhost:8000
'''
body[api] =
body[args] =
'''
async def run_api(body: Any) -> Any:
    result = {}

    try:
        api = body["api"]
        args = body["args"]

        result = await api_dict[api](args)
    
    except Exception as e:
        text = str(type(e).__name__ + " " + str(e))
        result['api'] = 'api'
        result['args'] = text

        logger.exception("Unhandled exception: " + text)
        #raise

    finally:
        return result
