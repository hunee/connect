#print('__FILE__: ', __file__)

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
    ASGIApp,
    Receive,
    Scope,
    Send,
    DecoratedCallable
)

import asyncio

import logging
import traceback
import sys

import ujson


###
from .routing import run_api


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


class Connect():
    def __init__(self, debug: bool = False) -> None:
        pass

    async def read_body(self, receive: Receive) -> str:
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

        """
        Echo the request body back in an HTTP response.
        """
        body = await self.read_body(receive)
        if body == b'':
            return

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


