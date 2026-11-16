import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import RAW_DATA_PATH, BRONZE_PATH, SILVER_PATH, GOLD_PATH
from src.extraction.read_data import get_spark_session, extract_orders
from src.transformation.cleaning import clean_orders
from src.validation.quality_checks import validate_orders
from src.loading.write_data import write_parquet, write_to_postgres
from pyspark.sql.functions import sum

def run_pipeline():
    spark = get_spark_session()
    spark.sparkContext.setLogLevel("ERROR")
    
    print("=== 1. BRONZE LAYER (Extract) ===")
    raw_df = extract_orders(spark, RAW_DATA_PATH)
    write_parquet(raw_df, BRONZE_PATH)
    
    print("=== 2. SILVER LAYER (Clean & Validate) ===")
    clean_df = clean_orders(raw_df)
    validate_orders(clean_df)
    write_parquet(clean_df, SILVER_PATH)
    
    print("=== 3. GOLD LAYER (Aggregate) ===")
    gold_df = clean_df.groupBy("status").agg(
        sum("revenue").alias("total_revenue")
    )
    gold_df.show()
    write_parquet(gold_df, GOLD_PATH)
    
    print("=== 4. LOAD TO POSTGRESQL ===")
    jdbc_url = "jdbc:postgresql://localhost:5432/hospital_db"
    properties = {
        "user": "postgres",
        "password": "postgres",
        "driver": "org.postgresql.Driver"
    }
    
    try:
        write_to_postgres(gold_df, "spark_revenue_summary", jdbc_url, properties)
    except Exception as e:
        print(f"Could not write to Postgres (Driver missing?): {e}")
    
    spark.stop()

if __name__ == "__main__":
    run_pipeline()
