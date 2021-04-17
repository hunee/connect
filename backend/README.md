#
# Asyncio WEB server
#

- backend
  - python 3.9
    - asyncio
    - uvicorn (ASGI)
    - sqlalchemy 1.4

    - "POST / HTTP/1.1"
    - body parser
      - json
      - routing
      - gzip - ???

  - nodejs
    - "POST / HTTP/1.1"
    - body parser
      - json
      - routing

- db
  - mysql
  - alembic

- redis

- proxy
  - nginex

- admin
  - FastAPI
  
- Docker


$ uvicorn app.main:app --reload --log-config ./config/logging.yaml
or
$ python3 -m app --host 0.0.0.0 --port 8000

$ server.sh --host 0.0.0.0 --port 8000


