#
#
#

docker-compose up -d 
docker-compose up -d --build
docker-compose up -d --force-recreate

docker-compose up -d --build --no-recreate 
docker-compose up -d --build --force-recreate --renew-anon-volumes 

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

docker exec -it connect_backend_1 bash