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

from connect.types import (
    ASGIApp,
    Receive,
    Scope,
    Send,
    DecoratedCallable
)

import logging
import traceback

import aiohttp
import requests

###
import connect


#from ..models import user
from .. import models

logger = logging.getLogger(__name__)

#curl -d '{"api":"ren_user", "args":{"type":"a", "text":"b"}}' -H "Content-Type: application/json" -X POST http://localhost:8000

@connect.api
#async def add_user(json_data: Any) -> typing.Callable:
async def ren_user(args: Any) -> typing.Callable:   
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('user', 'pass')
    ) as session:
        async with session.get('https://api.github.com/user', ssl=False) as resp:
            print(resp.status)
            body = await resp.text()
            print(body)

    return args


