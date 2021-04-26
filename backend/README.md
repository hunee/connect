#
# Python WEB server
#

- backend
  - python 3.9
    
    - asyncio, uvloop
    - cython, c/c++

    - db
      - SQLAlchemy 1.4
      - mysql

    - asgi
      - uvicorn
        - websockets
        - httptools

    - starlette
    - fastapi

    - routing
      - HTTP POST/1.1
      - websocket
      
      - base64, md5, jwt
      - json
        - orjson
        - ujson

  - nodejs
    - connect
      - routing
        - HTTP POST/1.1

      - db
        - mysql2

  - boost
    - asio

  - db
    - mysql
    - alembic

  - redis

- proxy
  - nginex

- admin
  - FastAPI
  
- Docker


uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-config ./logging.yaml

python3 ./serve.py --host 0.0.0.0 --port 8000

server.sh --host 0.0.0.0 --port 8000


