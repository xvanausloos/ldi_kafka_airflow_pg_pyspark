from pyspark.sql import SparkSession
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(funcName)s:%(levelname)s:%(message)s"
)

# Create a Spark session
spark = SparkSession.builder.appName("KafkaToDelta").getOrCreate()

logging.info("Spark session created successfully")

# Read data from Kafka
topic_name = "topic1"
kafka_stream = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "topic1")
    .option("startingOffsets", "earliest")
    .load()
)
logging.info(f"Kafka read the stream in topic:{topic_name}")



# Transform the Kafka stream (e.g., extract the value and cast to String)
kafka_values = kafka_stream.selectExpr("CAST(value AS STRING)")

logging.info(f"Kafka values: {kafka_values}")

query = kafka_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()


# Write the transformed stream to a Delta table
# delta_location = "tmp/delta-table"
# checkpoints_location = "tmp/checkpoints"
# kafka_values.writeStream.format("delta").outputMode("append").option(
#     "checkpointLocation", checkpoints_location
# ).start("tmp/delta-table")
#
# logging.info(f"Stream written in Delta table to {delta_location} ")


