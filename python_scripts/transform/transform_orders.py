import pandas as pd


def transform_orders(df):
    df = df.copy()

    # Standardize columns
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Convert types
    df["order_id"] = pd.to_numeric(df["order_id"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Clean text
    df["status"] = df["status"].str.strip().str.lower()

    # Drop rows missing critical data
    df = df.dropna(subset=["order_id", "quantity", "unit_price"])

    # Calculate total
    df["total_amount"] = df["quantity"] * df["unit_price"]

    print(f"Transformed data. {len(df)} valid rows remaining.")
    return df
