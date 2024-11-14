import unittest
from unittest.mock import patch
from pyspark.sql import Row, SparkSession
from pyspark.sql.streaming import DataStreamWriter

class TestPySparkStreaming(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup Spark session for the tests."""
        cls.spark = SparkSession.builder \
            .master("local[1]") \
            .appName("PySparkStreamingTest") \
            .getOrCreate()

    def test_kafka_stream_processing(self):
        """Test Kafka stream processing and Delta table write."""
        sample_data = [Row(value="test_message_1"), Row(value="test_message_2")]

        # Create a DataFrame with mocked Kafka input data
        kafka_df = self.spark.createDataFrame(sample_data)

        # Mock the Kafka read stream
        with patch('pyspark.sql.SparkSession.readStream') as mock_read_stream:
            mock_read_stream.return_value = kafka_df

            # Simulate calling the function that reads from Kafka and processes the stream
            kafka_values = kafka_df.selectExpr("CAST(value AS STRING)")

            # Mock the write operation
            with patch.object(DataStreamWriter, 'start') as mock_write_stream:
                # Perform the write
                kafka_values.writeStream.format("delta").outputMode("append").start("tmp/delta-table")

                # Assert that the DataFrame was correctly transformed
                transformed_data = [row['value'] for row in kafka_values.collect()]
                self.assertEqual(transformed_data, ["test_message_1", "test_message_2"])

                # Assert that the write operation was triggered once
                mock_write_stream.assert_called_once()

    @classmethod
    def tearDownClass(cls):
        """Stop the Spark session after the tests."""
        cls.spark.stop()

if __name__ == '__main__':
    unittest.main()