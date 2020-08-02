mysql="mysql:8.0"
# rentalServer="andrew54068/rental-server-side:latest"

docker run \
--restart always \
--name mysql-rental \
-v /Users/upn/Documents/self\ project/rentalRadar/rentalServerSide/rentalDB:/var/lib/mysql \
-v /Users/upn/Documents/self\ project/rentalRadar/rentalServerSide/docker/my.cnf:/etc/mysql/my.cnf \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=password \
-e MYSQL_SECRET=password \
-d $mysql

# docker run \
# --name rental-server \
# -p 5000:5000 \
# --env-file ./.env \
# -d $rentalServer