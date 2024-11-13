# PySpark unit tests

## Prerequisites for running `kafka_stream_delta.py` using Docker
- Kafka instance in Docker. 

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
- Install Kafka cli locally instance 
Run locally:
`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,io.delta:delta-core_2.12:2.1.0 utests/kafka_pyspark_delta.py`

Job running b