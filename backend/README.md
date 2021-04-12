$ mysql -u root -p P9 < P9_2014-02-20.sql 

- backend
  - python 3.9
    - Connect 0.0.1
      - pip install uvicorn (ASGI)
      - pip install uvloop

      - "POST / HTTP/1.1"
      - body parser
        - json
        - gzip
        - routing
      
    - Logger
    - Database
      - sqlalchemy 1.4
      - mysql

- db
  - mysql

- redis

- proxy
  - nginex

- FastAPI
- Docker



git clone https://github.com/encode/uvicorn
git clone https://github.com/encode/starlette
git clone https://github.com/tiangolo/fastapi

pip freeze | xargs pip uninstall -y

pip3 freeze > requirements.txt
pip3 install -r requirements.txt

pip3 install aiomysql
pip3 install aioredis
pip3 install PyYAML
pip3 install SQLAlchemy
pip3 install ujson
pip3 install uvicorn
pip3 install uvloop

pip3 install aiohttp
pip3 install requests


$ uvicorn app.main:app --reload --log-config ./config/logging.yaml
$ python3 -m app

docker-compose up -d 
docker-compose up -d --build
docker-compose up -d --force-recreate

docker-compose down 
docker-compose down --volume

docker-compose start 
docker-compose stop

docker images
docker volume ls  

docker logs server_backend_1 

docker exec -it server_db_1 bash
$ mysql -u root -p

docker exec -it server_redis_1 redis-cli

