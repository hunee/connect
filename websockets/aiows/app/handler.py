print('__FILE__: ', __file__)

import asyncio
import json
import logging
import traceback
import sys



event_handlers = dict()
function_handlers = dict()

def event(fn):
    """
    Register a function to receive and handle events.
    """
    module = fn.__module__.split(".")[-1]
    key = module + "." + fn.__name__
    logging.info("Registering event handler: '" + key + "' from " + fn.__module__)

    fn = asyncio.coroutine(fn)
    event_handlers[key] = fn
    return fn


def function(fn):
    """
    Register a function to receive a request and return a result
    """
    module = fn.__module__.split(".")[-1]
    key = module + "." + fn.__name__
    logging.info("Registering function handler: '" + key + "' from " + fn.__module__)

    fn = asyncio.coroutine(fn)
    function_handlers[key] = fn
    return fn


@asyncio.coroutine
def handle_event(conn, msg):
    #print('>> def: ' + handle_event.__name__)

    name = msg["name"]
    args = msg["args"]
    #print('name: ', name)
    #print('args: ', args)

    try:
        yield from event_handlers[name](conn, *args)
        #event_handlers[name](c, **args)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)


@asyncio.coroutine
def handle_function(conn, msg):
    print('>> def: ' + handle_function.__name__)

    name = msg["name"]
    args = msg["args"]
    id = msg['id']

    #print('name: ', name)
    #print('args: ', args)

    try:
        result = yield from function_handlers[name](conn, *args)
        #print('result: ', str(result))

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        yield from conn.send('return', type=name, msg_=id, text=str(type(e).__name__ + " " + str(e)))
    else:
        yield from conn.send('return', type=name, msg_=id, text=result)


