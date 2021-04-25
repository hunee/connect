
git clone https://github.com/encode/uvicorn
git clone https://github.com/encode/starlette
git clone https://github.com/tiangolo/fastapi

git clone https://github.com/aio-libs/aiohttp
git clone https://github.com/aio-libs/aiomysql
git clone https://github.com/aio-libs/aioredis-py

git clone https://github.com/sqlalchemy/sqlalchemy/

git clone https://github.com/nackjicholson/aiosql

git clone https://github.com/python-hyper/wsproto/

git clone https://github.com/vibora-io/vibora

git clone https://github.com/MagicStack/httptools
git clone https://github.com/MagicStack/uvloop
git clone https://github.com/MagicStack/asyncpg

git clone https://github.com/python-hyper/h2

https://github.com/ijl/orjson

pip3 install .

pip freeze | xargs pip uninstall -y

pip3 freeze > requirements.txt
pip3 install -r requirements.txt

pip3 install PyYAML
pip3 install ujson
pip3 install orjson


pip3 install uvloop

pip3 install httptools
pip3 install websockets 

pip3 install h11
pip3 install wsproto

pip3 install uvicorn

pip3 install aiohttp
pip3 install requests

pip3 install SQLAlchemy

pip3 install alembic
pip3 install pydantic

pip3 install aiosql
pip3 install pypika

pip3 install pyjwt

pip3 install PyMySQL
pip3 install hiredis

async-timeout
typing-extensions