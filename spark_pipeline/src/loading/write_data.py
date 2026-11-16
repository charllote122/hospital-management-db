def write_parquet(df, path, mode="overwrite"):
    df.write.mode(mode).parquet(path)
    print(f"Data written to {path}")

def write_to_postgres(df, table_name, jdbc_url, properties):
    df.write.jdbc(
        url=jdbc_url,
        table=table_name,
        mode="append",
        properties=properties
    )
    print(f"Data written to PostgreSQL table {table_name}")
