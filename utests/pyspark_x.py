from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder.appName("PySpark x").getOrCreate()

csv_file = "../data/sample.csv"

df = spark.read.option("header", "true").option("inferSchema", "true").csv(csv_file)

print(df.show(truncate=False))
