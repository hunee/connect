import asyncio

import aiohttp
import requests

url = "http://localhost:5000"
header = {"Accept-Encoding": "gzip,deflate", "Content-Type":"application/json"}
data = '{"method":"add_user", "args":{"type":"a", "text":"b"}}'
#        {"method":"add_user", "args":{"type":"a", "text":"b", "user":"b"}}

async def main():
    async with aiohttp.ClientSession(
        auth=aiohttp.BasicAuth('user', 'pass')
    ) as session:
        async with session.post(url, headers=header, data=data, ssl=False) as resp:
            print(resp.status)
            body = await resp.text()
            print(body)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())