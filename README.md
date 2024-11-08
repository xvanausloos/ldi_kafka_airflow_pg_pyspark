# LDI end to end Data Eng project 
Use Kafka, PySpark, Airflow, PG
Created on Nov 24.
Source: https://towardsdatascience.com/end-to-end-data-engineering-system-on-real-data-with-kafka-spark-airflow-postgres-and-docker-a70e18df4090

## Create and enable venv
`python -m .venv venv`
`source .venv/bin/activate`

## Infrastructure with Docker
Before running the kafka service, 
let’s create the airflow-kafka network using the following command:
`docker network create airflow-kafka`

Run `docker-compose -f infrastructure/docker-compose.yaml up -d
`
It will create:
- Kafka cluster

visit the kafka-ui at http://localhost:8000/

### Create a Kafka topic 
Thanks to UI create a topic

### Postgres setup thanks to Docker
run `docker-compose -f infrastructure/postgres14-docker-compose.yaml up -d
`
Check connection : `psql -h localhost -p 5432 -U admin -d test_db`
see in `postgres14-docker-compose.yaml` for the password.

### Create and populate PG table
Run `python scripts/create_table.py`








