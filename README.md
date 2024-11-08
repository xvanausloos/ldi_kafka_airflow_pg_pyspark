# LDI end to end Data Eng project 
Use Kafka, PySpark, Airflow, PG

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


