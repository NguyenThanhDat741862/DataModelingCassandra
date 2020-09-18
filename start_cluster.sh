#!/bin/bash

docker network create cassandra_net || true

docker-compose -f ./setup/docker-compose.yml up
