#print('__FILE__: ', __file__)

#
import logging
import typing

import ujson

####
logger = logging.getLogger(__name__)

_msg_methods = dict()

def method(func: typing.Callable) -> typing.Callable:
    #module = func.__module__.split(".")[-1]
    #key = module + "." + func.__name__
    key = func.__name__
    logger.info("->> method -> '" + key + "' from " + func.__module__)

    _msg_methods[key] = func
    return func

'''
def id_(id: str) -> Callable[[DecoratedCallable], DecoratedCallable]:
    def decorator(func: DecoratedCallable) -> DecoratedCallable:
        print(">> pid: '" + id + "' from " + func.__module__)

        api_dict[id] = func

        return func

    return decorator
'''

async def run_body(body: typing.Any) -> typing.Any:
    result = {}

    try:
        method = body["method"]
        args = body["args"]

        result = await _msg_methods[method](args)
    
    except Exception as e:
        text = str(type(e).__name__ + " " + str(e))
        result['method'] = 'run_body()'
        result['args'] = text

        logger.exception("Unhandled exception: " + text)
        #raise

    finally:
        return result
