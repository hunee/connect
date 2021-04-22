#print('__FILE__: ', __file__)

import typing
import logging

import aiohttp
import requests

import aioredis

###
import connect

from app.config import config, get_redis_url
from app.models import user

logger = logging.getLogger(__name__)

REDIS_URL = get_redis_url(config('mysql'))
pool = aioredis.ConnectionPool.from_url(REDIS_URL, max_connections=4)

#curl -d '{"api":"add_user", "args":{"type":"a", "text":"b"}}' -H "Content-Type: application/json" -X POST http://localhost:8000

@connect.method
#async def add_user(json_data: Any) -> typing.Callable:
async def add_user_1(args: typing.Any) -> typing.Callable:   
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('user', 'pass')
    ) as session:
        async with session.get('https://api.github.com/user', ssl=False) as resp:
            print(resp.status)
            body = await resp.text()
            print(body)

    return args


#curl -d '{"api":"del_user2", "args":{"type":"a", "text":"b", "trash":"true"}}' -H "Content-Type: application/json" -X POST http://localhost:8000

@connect.method
async def add_user_2(args: typing.Any):
    print('API: del_user: ', args['text'])  

    r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
    print('status_code: ', r.status_code)
    print('headers: ', r.headers['content-type'])
    print('encoding: ', r.encoding)
    print('text: ', r.text)
    print('json: ', r.json())
    return args


#curl -d '{"api":"del_user", "args":{"type":"a", "text":"b", "trash":"true"}}' -H "Content-Type: application/json" -X POST http://localhost:8000
@connect.method
async def add_user(args: typing.Any):
    print('====================< del_user: ', args['text'])  

    # 1. db에 저장
    await user.add_user()

    # 2. redis 에 저장
    async with aioredis.Redis(connection_pool=pool) as conn:
        await conn.set("life", 420)
        life = await conn.get('life')
        print(f"The answer: {life}")

    return args


