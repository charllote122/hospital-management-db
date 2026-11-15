import psycopg2
from config.settings import DB_CONFIG


def load_orders(df):
    # We explicitly map the DB_CONFIG keys to what psycopg2 expects
    conn_params = {
        "host": DB_CONFIG["host"],
        "port": DB_CONFIG["port"],
        "dbname": DB_CONFIG["dbname"],
        "user": DB_CONFIG["user"],
        "password": DB_CONFIG["password"],
    }

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # Create table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cleaned_orders (
                    order_id BIGINT PRIMARY KEY,
                    customer_id BIGINT,
                    order_date TIMESTAMP,
                    product TEXT,
                    quantity INTEGER,
                    unit_price NUMERIC(12,2),
                    status TEXT,
                    total_amount NUMERIC(14,2)
                );
            """)

            # Insert data
            records = df[
                [
                    "order_id",
                    "customer_id",
                    "order_date",
                    "product",
                    "quantity",
                    "unit_price",
                    "status",
                    "total_amount",
                ]
            ].itertuples(index=False, name=None)

            for row in records:
                cur.execute(
                    """
                    INSERT INTO cleaned_orders (order_id, customer_id, order_date, product, quantity, unit_price, status, total_amount)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (order_id) DO NOTHING;
                """,
                    row,
                )
        # psycopg2 commits automatically when exiting the 'with' block

    print(f"Loaded {len(df)} records into PostgreSQL.")
