# LDI end to end Data Eng project 
Use Kafka, PySpark, Airflow, PG
Created on Nov 24.
Source: https://towardsdatascience.com/end-to-end-data-engineering-system-on-real-data-with-kafka-spark-airflow-postgres-and-docker-a70e18df4090

## Create and enable venv
`python -m .venv venv`
`source .venv/bin/activate`

## Kafka infrastructure with Docker
Before running the kafka service, 
let’s create the airflow-kafka network using the following command:
You can run `make create-kafka-infra`

It will create:
- Kafka cluster

visit the kafka-ui at http://localhost:8000/

### Create a Kafka topic 
Thanks to UI create a topic

### Install Postgres locally (without Docker)
see dedicated LDI doc.
Start Postgresql local instance:
`brew services start postgresql@14`

Check connection to PGADMIN:
connect to local PG instance: 
```
psql -d postgres
```

You can check tables using PgAdmin app installed locally in your Mac.

### Create and populate PG table
Run `python scripts/create_table.py` or use `make create-postgres-table`

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

## Addition of unit tests
Example: https://medium.com/@sharadblog/unit-testing-pyspark-kafka-streams-14746ca28dfe

See `kafka_pyspark_delta.py`
Run unit tests: from venv terminal: `pytest`

One test will run successfully.

## Monitoring Airflow with Grafana
Resource: https://medium.com/@perkasaid.rio/monitoring-airflow-metrics-with-grafana-29ebb43100a3

In Docker compose add these settings:
```
AIRFLOW__SCHEDULER__STATSD_ON: 'true'
AIRFLOW__SCHEDULER__STATSD_HOST: statsd-exporter
AIRFLOW__SCHEDULER__STATSD_PORT: 8125
AIRFLOW__SCHEDULER__STATSD_PREFIX: airflow
```
Installing Statsd-exporter: this is the bridge between Airflow and Prometheus
Add a service in the docker-compose file:
```
statsd-exporter:
        image: prom/statsd-exporter
        container_name: airflow-statsd-exporter
        command: "--statsd.listen-udp=:8125 --web.listen-address=:9102"
        ports:
            - 9102:9102
            - 8125:8125/udp
```
Rebuild the image:
`make create-airflow-infra`

you can go to http://127.0.0.1:9102 to check metrics that send to statsd-exporter

Addition of Prometheus to Docker compose:
```
prometheus:
    image: prom/prometheus
    container_name: airflow-prometheus
    ports:
        - 9090:9090
    volumes:
        - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
```
Add a file `prometehus.yaml` in `infrastructure\prometheus`
Run: `make create-airflow-infra`

Open Prometheuse UI: `localhost:9090`
You can see the Airflow Statsd endpoint in `http://127.0.0.1:9090/targets`

## Grafana install
Add a new service in `airflow-docker-compose.yaml`
Run: `make create-airflow-infra`

Access to Grafana UI: 
`https://localhost:3000`
Login with default user `grafana` and password `grafana`


