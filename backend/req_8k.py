import asyncio

import aiohttp
import requests

import ujson

url = "http://localhost:8000"
header = {"Accept-Encoding": "gzip,deflate", "Content-Type":"application/json"}


class Message:
    def __init__(self, T):
        self.T = T()

    @property
    def dict(self):
        return dict(method = type(self.T).__name__, kwargs = self.T.__dict__)

    def dumps(self):
        json = dict(method = type(self.T).__name__, args = self.T.__dict__)
        json_str = ujson.dumps(json)
        json_str.encode("utf-8")

        print('json: ' + json_str)


class add_user():
    def __init__(self):
        self.type = 'body.idhkjfhdskfhkshkf'
        self.text = 'textfkdjsfhkjshkfjdshfskjh'
        self.uname2 = 'unameghfgjsdgfjhsfgsdjhfgs'


req = Message(add_user)
req.T.uname = 'body.data'

async def main():
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('user', 'pass')
    ) as session:

        json_str = ujson.dumps(req.dict)
        json_str.encode("utf-8")

        print('json: ' + json_str)

        async with session.post(url, headers=header, data=json_str, ssl=False) as resp:
            print(resp.status)
            body = await resp.text()
            print(body)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())