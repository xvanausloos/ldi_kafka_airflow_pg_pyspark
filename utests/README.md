# Prerequisites
- Kafka instance in Docker. 
- Install locally in Mac Book hadoop:
`brew install hadoop`
- Export to path:
```
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH
export HADOOP_HOME=/opt/homebrew/Cellar/hadoop/3.4.1/bin 
```
Run locally:
`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,io.delta:delta-core_2.12:2.1.0 utests/kafka_pyspark_delta.py`
