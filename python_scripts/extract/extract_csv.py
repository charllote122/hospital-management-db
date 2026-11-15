import pandas as pd
from pathlib import Path


def extract_orders(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")
    if path.stat().st_size == 0:
        raise ValueError("Source file is empty")

    df = pd.read_csv(path)
    print(f"Extracted {len(df)} records from CSV")
    return df
