#!/bin/bash

# rm -r ./setup/docker/volumes/cassandra_data_seed/*
# rm -r ./setup/docker/volumes/cassandra_data_node/*

docker network create cassandra_net || true

docker-compose -f ./setup/docker-compose.yml up
