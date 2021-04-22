#print('__FILE__: ', __file__)

import asyncio
import logging
import typing

import ujson

from starlette.types import ASGIApp, Receive, Scope, Send

from .routing import run_api

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


class Post():
    def __init__(self, debug: bool = False) -> None:
        pass

    async def _read_body(self, receive: Receive) -> bytes:
        """
        Read and return the entire body from an incoming ASGI message.
        """
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return body

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        #print('scope: ', scope)

        assert scope["type"] in ("http", "websocket")
        assert scope["method"] == "POST"

        """
        Echo the request body back in an HTTP response.
        """
        body = await self._read_body(receive)
        if body == b'':
            return

        headers = dict(scope['headers'])

        logger.info('headers: ' + str(headers))
        logger.info('->> headers[authorization]: ' + str(headers[b'authorization']))

        logger.info('->> scope: ' + str(scope))
        logger.info('->> body: ' + str(body))
        

        result = {}

        try:
            json_body = ujson.loads(body)
            
            result = await run_api(json_body)

        except Exception as e:
            msg = str(type(e).__name__ + " " + str(e))  
            result['api'] = 'api'
            result['args'] = 'args'

            logger.exception("Unhandled exception: " + msg)
            #raise
              
        send_json_str = ujson.dumps(result)
        logger.info('<<- send_json_str: ' + send_json_str)

        '''
        '''
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


