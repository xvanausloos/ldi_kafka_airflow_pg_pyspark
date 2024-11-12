from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)

# Create a Spark session
spark = SparkSession.builder \
    .appName("KafkaToDelta") \
    .getOrCreate()

logging.info("Spark session created successfully")

# Read data from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "rappel_conso") \
    .load()
logging.info("Kafka read the stream rappel conso")

# Transform the Kafka stream (e.g., extract the value and cast to String)
kafka_values = kafka_stream.selectExpr("CAST(value AS STRING)")

logging.info(f"Kafka values: {kafka_values}")
logging.debug(kafka_values.show(truncate=False))

# Write the transformed stream to a Delta table
delta_location = "/tmp/delta-table"
checkpoints_location = "/tmp/checkpoints"
kafka_values.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", checkpoints_location) \
    .start(delta_location)

logging.info("Stream written in Delta table to {delta_location} ")
