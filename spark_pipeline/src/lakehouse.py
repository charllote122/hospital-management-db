import os
import sys
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import col

# Windows fixes
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ["PATH"]

# 1. Start Spark with Delta Lake extensions
builder = (
    SparkSession.builder.appName("HospitalLakehouse")
    .master("local[*]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    .config("spark.hadoop.hadoop.home.dir", "C:/hadoop")
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
    .config(
        "spark.jars",
        "file:///C:/dev/hospital-management-db/spark_pipeline/jars/postgresql-42.7.14.jar",
    )
)

spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# 2. Read the data from your existing Parquet Bronze layer
bronze_path = "spark_pipeline/data/bronze/orders"
print("Reading data from Bronze layer...")
df = spark.read.parquet(bronze_path)

# 3. Write to a Delta table
lakehouse_path = "spark_pipeline/data/lakehouse/orders_delta"
print("Writing data to Delta Lake...")

df.write.format("delta").mode("overwrite").save(lakehouse_path)

print(f"✅ Delta table created at {lakehouse_path}")

# 4. Verify
print("\n=== Reading from Delta Table ===")
delta_df = spark.read.format("delta").load(lakehouse_path)
delta_df.show()

# 5. ACID Update
print("\n=== Updating a record (ACID transaction) ===")
from delta.tables import DeltaTable
delta_table = DeltaTable.forPath(spark, lakehouse_path)
delta_table.update(condition="order_id = 1003", set={"status": "'completed'"})
print("✅ Updated order 1003 to 'completed'")

# 6. Time Travel
print("\n=== Time Travel to Version 0 (before the update) ===")
old_df = spark.read.format("delta").option("versionAsOf", 0).load(lakehouse_path)
old_df.filter(col("order_id") == 1003).show()

print("=== Current Version (after the update) ===")
delta_df = spark.read.format("delta").load(lakehouse_path)
delta_df.filter(col("order_id") == 1003).show()

spark.stop()
