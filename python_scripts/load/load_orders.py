import psycopg
from config.settings import DB_CONFIG


def load_orders(df):
    with psycopg.connect(**DB_CONFIG) as conn:
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

    print(f"Loaded {len(df)} records into PostgreSQL.")
