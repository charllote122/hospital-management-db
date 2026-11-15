def validate_orders(df):
    if (df["quantity"] <= 0).any():
        raise ValueError("Invalid quantities detected (<= 0)")
    if (df["unit_price"] < 0).any():
        raise ValueError("Negative unit prices detected")
    print("Validation successful. No bad data found.")
    return True
