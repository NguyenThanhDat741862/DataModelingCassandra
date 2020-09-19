
start-cluster:
	docker network create cassandra_net || true
	docker-compose -f ./setup/docker-compose.yml up

shutdown-cluster:
	docker rm -f cassandra-node
	docker rm -f cassandra-seed
	docker network rm cassandra_net

reset-volume-cluster:
	rm -r ./setup/docker/volumes/cassandra_data_seed/*
	rm -r ./setup/docker/volumes/cassandra_data_node/*

setup-env:
	cd ./project && \
	pipenv install

run:
	cd ./project && \
	pipenv run python3 main.py

