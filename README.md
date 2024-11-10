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
You can run `make create-kafka-infra`

It will create:
- Kafka cluster

visit the kafka-ui at http://localhost:8000/

### Create a Kafka topic 
Thanks to UI create a topic

### Postgres setup thanks to Docker
Run `make make create-postgresql-infra`

### Create and populate PG table
Run `python scripts/create_table.py`

### Run Docker for creating infra for Spark job
Run from root folder:
`docker build -f infrastructure/spark-dockerfile.yaml
-t rappel-conso/spark:latest 
--build-arg POSTGRES_PASSWORD=$POSTGRES_PASSWORD  .`

This command will build the image rappel-conso/spark:latest. 
This image includes everything needed to run our Spark job 
and will be used by Airflow’s DockerOperator to execute the job. 

### Airflow
In our system, Airflow is used to automate the data flow from streaming 
with Kafka to processing with Spark.

#### Airflow infra 
Run `echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_PROJ_DIR=\"./airflow_resources\"" > .env`
It creates a `.env` file with env variables for Airflow.
Create a folder `airflow_resources`

Go in `airflow_resources` folder:
run `docker build -t airflow-ldi:1.0 .`
It will create locally the Docker images customized by LDI.

Run `make create-airflow-infra`

#### Airflow UI
Connect to `http://localhost:8080`
Credentials are: airflow/aiflow 

## Pipeline
Check Airflow DAG : `kafka_spark_dag`





