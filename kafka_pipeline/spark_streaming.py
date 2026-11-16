import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, sum
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    DoubleType,
    TimestampType,
)

# Windows fixes
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"

# 1. Start Spark with the Kafka connector (use the latest stable 3.5.0 version)
spark = (
    SparkSession.builder.appName("KafkaStreamingToPostgres")
    .master("local[*]")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
    .config(
        "spark.jars",
        "C:/dev/hospital-management-db/spark_pipeline/jars/postgresql-42.7.14.jar",
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# 2. Define the event schema
event_schema = StructType(
    [
        StructField("event_id", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("patient_id", IntegerType(), True),
        StructField("doctor_id", IntegerType(), True),
        StructField("amount", IntegerType(), True),
        StructField("status", StringType(), True),
        StructField("timestamp", StringType(), True),
    ]
)

# 3. Read the stream from Kafka
print("Connecting to Kafka...")
stream_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "orders")
    .option("startingOffsets", "earliest")
    .load()
)

# 4. Parse the binary Kafka data into structured columns
parsed_df = (
    stream_df.select(
        col("key").cast("string").alias("patient_key"),
        col("value").cast("string").alias("json_value"),
        "topic",
        "partition",
        "offset",
    )
    .withColumn("event", from_json("json_value", event_schema))
    .select("patient_key", "topic", "partition", "offset", "event.*")
)

# 5. Aggregate the stream (total amount per patient)
print("Aggregating stream...")
aggregated_df = parsed_df.groupBy("patient_id").agg(sum("amount").alias("total_billed"))

# 6. Write the stream to the console
query = (
    aggregated_df.writeStream.outputMode("complete")
    .format("console")
    .option("truncate", "false")
    .option("checkpointLocation", "data/checkpoints")
    .start()
)

print("Streaming started. Waiting for events...")
query.awaitTermination()
