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
$ python3 -m app

$ server.sh


find . -name .DS_Store -print0 | xargs -0 git rm --ignore-unmatch

$ vi ~/.gitignore_global
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

.DS_Store
._.DS_Store
**/.DS_Store
**/._.DS_Store

$ git config --global core.excludesfile ~/.gitignore_global
