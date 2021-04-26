import asyncio

import aiohttp
import requests

import json
import ujson
import orjson

import base64
import hashlib


url = "http://localhost:8000"
header = {"Accept-Encoding": "gzip,deflate", "Content-Type":"text/plain"}


class Message:
    def __init__(self, T):
        self.T = T()

    @property
    def dict(self):
        return dict(pid = type(self.T).__name__, kwargs = self.T.__dict__)

    def dumps(self):
        json = dict(pid = type(self.T).__name__, args = self.T.__dict__)
        json_str = ujson.dumps(json)
        json_str.encode("utf-8")

        print('json: ' + json_str)


class REQ_ADD_USER():
    def __init__(self):
        self.type = 'body.idhkjfhdskfhkshkf'
        self.text = 'textfkdjsfhkjshkfjdshfskjh'
        self.uname2 = 'unameghfgjsdgfjhsfgsdjhfgs'


req = Message(REQ_ADD_USER)
req.T.uname2 = 'body.data'

async def main():
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('user', 'pass')
    ) as session:

        json_send_str = ujson.dumps(req.dict)
        print('->> json_send_str: ' + json_send_str)

        send_base64_encoded = base64.b64encode(json_send_str.encode('utf-8'))
        print('->> send_base64_encoded: ' + str(send_base64_encoded))

        async with session.post(url, headers=header, data=send_base64_encoded, ssl=False) as resp:
            print(resp.status)
            body = await resp.text()

            json_text = base64.b64decode(body).decode('utf-8')
            print('->> json_text: ', json_text)

            json_body = orjson.loads(json_text)
            print('->> json_body: ', json_body)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())