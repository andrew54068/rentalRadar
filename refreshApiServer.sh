#!/bin/bash

docker build -t andrew54068/rental-server-side:latest .
docker push andrew54068/rental-server-side:latest
export ENV_FILE=./.env.dev 
docker-compose -f docker-compose.yml -f docker-compose.debug.yml pull rental-server-side
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up