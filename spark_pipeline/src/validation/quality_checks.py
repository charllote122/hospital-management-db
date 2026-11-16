from pyspark.sql.functions import col

def validate_orders(df):
    # Check for negative revenue
    invalid = df.filter(col("revenue") < 0)
    if invalid.count() > 0:
        raise ValueError("Negative revenue detected!")
    print("Validation passed: No negative revenue.")
    return df
