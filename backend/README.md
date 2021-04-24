#
# Asyncio "POST / HTTP/1.1" WEB server
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


uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-config ./logging.yaml

python3 ./serve.py --host 0.0.0.0 --port 8000

server.sh --host 0.0.0.0 --port 8000


