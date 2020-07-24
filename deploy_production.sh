#!/bin/bash
# define env var default value.
export ENV_FILE=./.env

docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up