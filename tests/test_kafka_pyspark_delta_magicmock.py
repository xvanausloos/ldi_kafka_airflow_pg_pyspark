import unittest
from unittest.mock import patch, MagicMock
from pyspark.sql import Row
from pyspark.sql.streaming import DataStreamWriter
from pyspark.sql import SparkSession


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
        # Sample data to mock the Kafka input
        sample_data = [Row(value="test_message_1"), Row(value="test_message_2")]
        kafka_df = self.spark.createDataFrame(sample_data)

        # Mock the readStream method to return a streaming DataFrame
        with patch('pyspark.sql.SparkSession.readStream') as mock_read_stream:
            # Create a MagicMock to simulate the streaming DataFrame
            mock_stream_df = MagicMock()
            # Simulate the streaming DataFrame returning the data we want
            mock_stream_df.selectExpr.return_value = kafka_df.selectExpr("CAST(value AS STRING)")
            mock_read_stream.return_value = mock_stream_df

            # Call the transformation on the DataFrame (simulating processing)
            kafka_values = mock_stream_df.selectExpr("CAST(value AS STRING)")

            # Mock the write operation
            with patch.object(DataStreamWriter, 'start') as mock_write_stream:
                # Simulate the writeStream operation
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
