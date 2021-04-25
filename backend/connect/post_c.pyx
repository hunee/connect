#print('__FILE__: ', __file__)

import asyncio
import logging
import typing

import ujson

from starlette.types import ASGIApp, Receive, Scope, Send

from .method import run_body

###
logger = logging.getLogger(__name__)

async def app_get_put(scope, receive, send):
    """Documentation for a function.

    More details.
    """

    """
    Echo the method and path back in an HTTP response.
    """
    assert scope['type'] == 'http'

    print('scope: ', scope)

    body = f'Received {scope["method"]} request to {scope["path"]}'
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': body.encode('utf-8'),
    })


async def _read_body(receive: Receive) -> bytes:
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    #cdef char * body = ''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body

async def asgi(scope: Scope, receive: Receive, send: Send) -> None:
    #print('scope: ', scope)

    assert scope["type"] in ("http", "websocket")
    assert scope["method"] == "POST"

    ###
    logger.info('->> scope: ' + str(scope))

    ###headers = dict(scope['headers'])
    ###logger.info('->> headers: ' + str(headers))
    ###logger.info('->> headers[authorization]: ' + str(headers[b'authorization']))

    """
    Echo the request body back in an HTTP response.
    """
    body = await _read_body(receive)
    if body == b'':
        return

    logger.info('->> body: ' + str(body))
    

    ###
    result = {}

    try:
        json_body = ujson.loads(body)
        
        result = await run_body(json_body)

        send_json_str = ujson.dumps(result)
        logger.info('<<- send_json_str: ' + send_json_str)

    except Exception as e:
        msg = str(type(e).__name__ + " " + str(e))  
        result['method'] = 'postapi()'
        result['args'] = 'args'

        logger.exception("Unhandled exception: " + msg)
        #raise
            
    finally:
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'application/json'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': send_json_str.encode('utf-8'),
        })    


