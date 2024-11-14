# PySpark unit tests sample

## Prerequisites for running `kafka_stream_delta.py` using Docker
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
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,io.delta:delta-core_2.12:2.2.0 \
--conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" \
--conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog" \
src/spark_pgsql/kafka_pyspark_delta.py
```
NB: Spark version has to match org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 version (3.5.3 in this example)



  