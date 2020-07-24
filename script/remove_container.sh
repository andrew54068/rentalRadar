mysql="mysql:8.0"
rentalServer="andrew54068/rental-server-side:latest"

docker ps -a -f ancestor=$mysql | xargs docker stop | xargs docker rm
docker ps -a -f ancestor=$rentalServer | xargs docker stop | xargs docker rm