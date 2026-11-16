from pyspark.sql.functions import col, expr

def clean_orders(df):
    # Filter out null quantities and calculate revenue
    clean_df = df.filter(col("quantity").isNotNull()) \
                 .withColumn("revenue", expr("quantity * unit_price"))
    return clean_df
