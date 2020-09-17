#!/bin/bash

docker rm -f cassandra-node
docker rm -f cassandra-seed
docker network rm cassandra_net
