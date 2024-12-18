# PySpark unit tests sample
Inspired from: https://medium.com/@sharadblog/unit-testing-pyspark-kafka-streams-14746ca28dfe

## Prerequisites for running `kafka_stream_delta.py` using Docker
- Spark version 3.3 max
- Kafka instance in Docker.
- Check you have access to Kafka UI: `http://localhost:8000/ui/clusters/local/all-topics/topic1`

## Prerequisites for running `kafka_stream_delta.py` locally
- Enable venv: `source .venv/bin/activate`
- Install Hadoop locally in Mac Book hadoop:
`brew install hadoop`
- Export to path:
```
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH
export HADOOP_HOME=/opt/homebrew/Cellar/hadoop/3.4.1/bin 
```
- Test connection to Kafka Docker instance (nb: port is 9094 check settings `kafka-docker-compose.yaml`:
`kafka-console-consumer --bootstrap-server localhost:9094 --topic topic1 --from-beginning`
- Install Kafka cli locally
- Cd in project root.
- Run
```
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,io.delta:delta-core_2.12:2.2.0 \
--conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
--conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
src/spark_pgsql/kafka_pyspark_delta.py
```
NB: Spark version has to match org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 version (3.3.0 in this example)

Using 
```
pip install parquet-cli
parq <file name>.parquet --head 10
``` 
you can check the content of the 
parquet files created in `delta-table` folder.

## Unit test 
For testing streaming with PySpark, To write a unit test for the given PySpark application that reads from Kafka, transforms the stream, and writes to a Delta table, you'll need to simulate the streaming data and verify the outputs. Since PySpark's streaming APIs don't have built-in test utilities 
like MemoryStream for Kafka sources, we can mock the Kafka input data.
From terminal in venv run:
`pytest` 

```
pytest  
============================================================================= test session starts ==============================================================================
platform darwin -- Python 3.9.6, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/xaviervanausloos/projects/ldi_kafka_airflow_pg_pyspark
collected 1 item                                                                                                                                                               

tests/test_kafka_pyspark_delta.py .                                                                                                                                      [100%]

============================================================================== 1 passed in 8.35s =
```
