#ifndef STAGE
#$(error STAGE is not set)
#endif

install-requirements:
	pip install -r requirements.txt

create-kafka-infra:
	docker network inspect airflow-kafka 2>&1>$null || docker network create airflow-kafka
	docker-compose -f infrastructure/kafka-docker-compose.yaml up -d

create-postgresql-infra:
	docker-compose -f infrastructure/postgres14-docker-compose.yaml up -d

create-airflow-infra:
	cd airflow_resources && docker build -t airflow-ldi:latest .
	docker compose -f infrastructure/airflow-docker-compose.yaml up -d
