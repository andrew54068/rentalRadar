#!/bin/bash

docker build -t andrew54068/rental-crawler:latest .
docker push andrew54068/rental-crawler:latest
export ENV_FILE=./.env.dev 
docker-compose -f docker-compose.yml -f docker-compose.debug.yml pull crawler
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up