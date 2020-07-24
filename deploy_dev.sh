#!/bin/bash
# define env var default value.
export ENV_FILE=./.env.dev

docker-compose -f docker-compose.yml -f docker-compose.debug.yml down
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
