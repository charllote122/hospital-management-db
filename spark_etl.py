import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DateType,
    DecimalType,
)

# CRITICAL FIX FOR WINDOWS
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# 1. Start Spark
spark = (
    SparkSession.builder.appName("HospitalSparkETL").master("local[*]").getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# 2. Define an explicit schema
# We tell Spark that quantity is an Integer, so 'NULL' becomes a real null
schema = StructType(
    [
        StructField("order_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("order_date", DateType(), True),
        StructField("product", StringType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("unit_price", DecimalType(10, 2), True),
        StructField("status", StringType(), True),
    ]
)

# 3. Read the CSV file with the explicit schema
csv_path = "python_scripts/data/raw/orders.csv"
print(f"Reading data from {csv_path}...")
df = spark.read.csv(csv_path, header=True, schema=schema)

print("=== Raw Data ===")
df.show()

# 4. Transform: Filter nulls and calculate revenue
# Because quantity is now a proper Integer, this will work perfectly
clean_df = df.filter(col("quantity").isNotNull()).withColumn(
    "revenue", expr("quantity * unit_price")
)

print("=== Cleaned Data with Revenue ===")
clean_df.show()

# 5. Aggregate: Total Revenue by Status
clean_df.createOrReplaceTempView("orders")

print("=== Total Revenue by Status ===")
spark.sql("""
    SELECT status, SUM(revenue) as total_revenue
    FROM orders
    GROUP BY status
    ORDER BY total_revenue DESC
""").show()

# 6. Stop Spark
spark.stop()
