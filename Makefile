#ifndef STAGE
#$(error STAGE is not set)
#endif

install-requirements:
	pip install -r requirements.txt

create-infra:
	docker network inspect airflow-kafka 2>&1>$null || docker network create airflow-kafka
	docker-compose -f infrastructure/docker-compose.yaml up -d

create-postgresql:
	docker-compose -f infrastructure/postgres14-docker-compose.yaml up -d
