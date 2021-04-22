import asyncio

import aiohttp
import requests

url = "http://localhost:80"
header = {"Accept-Encoding": "gzip,deflate", "Content-Type":"application/json"}
data = '{"api":"add_user", "args":{"type":"a", "text":"b"}}'


async def main():
    r = requests.post(url, headers=header, data=data, auth=('user', 'pass'))
    print('status_code: ', r.status_code)
    print('headers: ', r.headers['content-type'])
    print('encoding: ', r.encoding)
    print('text: ', r.text)
    print('json: ', r.json())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())