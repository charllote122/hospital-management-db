from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DateType,
    DecimalType,
)


def get_spark_session():
    return (
        SparkSession.builder.appName("HospitalPySparkPipeline")
        .master("local[*]")
        .config("spark.jars", "spark_pipeline/jars/postgresql-42.7.14.jar")
        .getOrCreate()
    )


def extract_orders(spark, path):
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

    df = spark.read.csv(path, header=True, schema=schema)
    return df
