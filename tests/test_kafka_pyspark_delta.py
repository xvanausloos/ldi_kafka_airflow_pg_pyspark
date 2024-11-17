import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row


@pytest.fixture(scope="session")
def spark():
    """
    Pytest fixture to initialize a SparkSession for testing.
    """
    return (
        SparkSession.builder.master("local[2]")
        .appName("PySparkUnitTest")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.jars.packages", "io.delta:delta-core_2.12:2.1.0")
        .getOrCreate()
    )


def transform_kafka_stream(input_df):
    """
    Function to transform the Kafka stream by casting value to STRING.
    """
    return input_df.selectExpr("CAST(value AS STRING)")


def test_kafka_to_delta(spark):
    """
    Unit test for the Kafka-to-Delta transformation.
    """
    from pyspark.sql.types import StructType, StructField, StringType

    # Mock Kafka input schema
    schema = StructType([StructField("value", StringType(), True)])

    # Mock input data (simulating Kafka messages)
    input_data = [Row(value="message1")]

    # Create a static DataFrame to simulate Kafka input
    input_df = spark.createDataFrame(input_data, schema)

    # Apply transformation
    transformed_df = transform_kafka_stream(input_df)

    # Verify the transformed schema
    expected_schema = StructType([StructField("value", StringType(), True)])
    assert transformed_df.schema == expected_schema

    # Mock Delta write by writing to a temporary path
    delta_path = "delta_table"
    transformed_df.write.format("delta").mode("overwrite").save(delta_path)

    # Read back the Delta table and verify the content
    result_df = spark.read.format("delta").load(delta_path)
    result_data = [row.asDict() for row in result_df.collect()]
    expected_data = [{"value": "message1"}]

    assert result_data == expected_data
