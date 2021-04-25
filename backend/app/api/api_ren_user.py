#print('__FILE__: ', __file__)

import typing
import logging

import aiohttp
import requests



###
import connect


#from ..models import user
from app.models import user

logger = logging.getLogger(__name__)

#curl -d '{"api":"ren_user", "args":{"type":"a", "text":"b"}}' -H "Content-Type: application/json" -X POST http://localhost:8000

@connect.method
#async def add_user(json_data: Any) -> typing.Callable:
async def ren_user(args: typing.Any) -> typing.Callable:   
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('user', 'pass')
    ) as session:
        async with session.get('https://api.github.com/user', ssl=False) as resp:
            print(resp.status)
            body = await resp.text()
            print(body)

    return args


