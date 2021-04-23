#print('__FILE__: ', __file__)

import asyncio
import logging
import typing

import ujson

from uvicorn.main import ServerState
from uvicorn.protocols.http.auto import AutoHTTPProtocol
from uvicorn.protocols.websockets.auto import AutoWebSocketsProtocol

from uvicorn.config import Config


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


from starlette.types import ASGIApp, Receive, Scope, Send

from .message import run_body

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


class post():
    def __init__(self, debug: bool = False) -> None:
        config = Config(app=self)

                
        policy = asyncio.get_event_loop_policy()
        assert isinstance(policy, asyncio.events.BaseDefaultEventLoopPolicy)
        expected_loop = "asyncio" if uvloop is None else "uvloop"
        assert type(policy).__module__.startswith(expected_loop)

        server_state = ServerState()
        protocol = AutoHTTPProtocol(config=config, server_state=server_state)
        expected_http = "H11Protocol" if httptools is None else "HttpToolsProtocol"
        assert type(protocol).__name__ == expected_http
        
        expected_http = "h11" if httptools is None else "httptools"

        protocol = AutoWebSocketsProtocol(config=config, server_state=server_state)
        expected_websockets = "WSProtocol" if websockets is None else "WebSocketProtocol"
        assert type(protocol).__name__ == expected_websockets
        
        expected_websockets = "wspro" if websockets is None else "websockets"
        
        logger.info(f'$$$ ------ START SERVER {config.host}:{config.port} --- {expected_loop}:{expected_http}:{expected_websockets} ------')

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

        ###
        logger.info('->> scope: ' + str(scope))

        ###headers = dict(scope['headers'])
        ###logger.info('->> headers: ' + str(headers))
        ###logger.info('->> headers[authorization]: ' + str(headers[b'authorization']))

        """
        Echo the request body back in an HTTP response.
        """
        body = await self._read_body(receive)
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


