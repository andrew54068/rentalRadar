#!/bin/bash
# define env var default value.
export ENV_FILE=./.env

docker-compose -f docker-compose.yml down
docker-compose rm -v

rm -rf mysql
mkdir mysql

docker-compose -f docker-compose.yml up