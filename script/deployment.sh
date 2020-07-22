docker run \
--restart always \
--name mysql-rental \
-v /home/ec2-user/rentalServerSide/rentalDB:/var/lib/mysql \
-v /home/ec2-user/rentalServerSide/docker/my.cnf:/etc/mysql/my.cnf \
-p 3307:3306 \
-d -e MYSQL_ROOT_PASSWORD=password \
mysql:8.0