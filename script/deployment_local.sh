mysql="mysql:8.0"
rentalServer="rentalserverside:latest"

docker ps -q -f ancestor=$mysql | xargs docker stop | xargs docker rm
docker ps -q -f ancestor=$rentalServer | xargs docker stop | xargs docker rm

docker run \
--restart always \
--name mysql-rental \
-v /Users/upn/Documents/self\ project/rentalRadar/rentalServerSide/rentalDB:/var/lib/mysql \
-v /Users/upn/Documents/self\ project/rentalRadar/rentalServerSide/docker/my.cnf:/etc/mysql/my.cnf \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=password \
-d $mysql

docker run \
--name rental-server \
--link mysql-rental \
-v /Users/upn/Documents/self\ project/rentalRadar/rentalServerSide:/app \
-p 5000:5000 \
--env-file ./rental.env \
-d $rentalServer 