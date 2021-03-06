#print('__FILE__: ', __file__)

import asyncio
import logging
import typing

import json
import ujson
import orjson

import base64
import hashlib


'''
try:
    import uvloop
except ImportError:  # pragma: no cover
    uvloop = None

try:
    import httptools
except ImportError:  # pragma: no cover
    httptools = None

try:
    import websockets
except ImportError:  # pragma: no cover
    # Note that we skip the websocket tests completely in this case.
    websockets = None
'''

from uvicorn.loops.auto import auto_loop_setup

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.websockets import WebSocket, WebSocketDisconnect

from starlette.routing import request_response, websocket_session
from starlette.routing import iscoroutinefunction_or_partial

from starlette.requests import Request
from starlette.responses import Response

from .routing import run_http_post, run_websocket
from .message import Message, response_exception

from .functools import function, function_async, profile


###
logger = logging.getLogger(__name__)

@function_async
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    
    except WebSocketDisconnect:
        pass

@function_async
async def http_endpoint(request: Request):
    content = '%s %s' % (request.method, request.url.path)

    return Response(content, media_type='text/plain')


@function_async
async def fast_http_post_endpoint(json_body):
    try:
        response = await run_http_post(json_body)

    except Exception as e:
        response = response_exception(e)

    finally:
        return response

@function_async
async def read_body(receive: Receive) -> bytes:
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


@function
def fast_request_response(func: typing.Callable) -> ASGIApp:
    """
    Takes a function or coroutine `func(request) -> response`,
    and returns an ASGI application.
    """
    is_coroutine = iscoroutinefunction_or_partial(func)

    @function
    async def app(scope: Scope, receive: Receive, send: Send) -> None:

        response = {}

        if scope["method"] == "POST":
            try:
                request_body = await read_body(receive)
                if request_body == b'':
                    return

                request_body_b64decode = base64.b64decode(request_body).decode('utf-8')
                json_body = orjson.loads(request_body_b64decode)

                if is_coroutine:
                    response = await func(json_body)
                else:
                    response = await run_in_threadpool(func, json_body)

            except Exception as e:
                response = response_exception(e)
                
            finally:
                pass


        #Response
        send_json_str = ujson.dumps(response)
        send_b64encoded = base64.b64encode(send_json_str.encode('utf-8'))

        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': send_b64encoded,
        })    

    return app


class Server():
    def __init__(self, debug: bool = False) -> None:
        #auto_loop_setup()

        '''
        policy = asyncio.get_event_loop_policy()
        assert isinstance(policy, asyncio.events.BaseDefaultEventLoopPolicy)
        expected_loop = "asyncio" if uvloop is None else "uvloop"
        assert type(policy).__module__.startswith(expected_loop)
        logger.info('->> LOOP: ' + expected_loop)

        expected_http = "h11" if httptools is None else "httptools"
        logger.info('->> HTTP: ' + expected_http)

        expected_websockets = "wsproto" if websockets is None else "websockets"
        logger.info('->> WEBSOCKETS: ' + expected_websockets)
        '''

        ###
        self.websocket = websocket_session(websocket_endpoint)
        self.http = fast_request_response(fast_http_post_endpoint)

        pass

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        assert scope["type"] in ("http", "websocket")

        if scope["type"] == "websocket":
            await self.websocket(scope, receive, send)

        elif scope["type"] == "http":
            await self.http(scope, receive, send)

        else:
            pass

