import json
import psycopg2
from confluent_kafka import Consumer

# 1. Database connection
db_config = {
    "host": "localhost",
    "port": 5432,
    "dbname": "hospital_db",
    "user": "postgres",
    "password": "postgres",
}


# 2. Create the table if it doesn't exist
def setup_db():
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS realtime_appointments (
                    event_id VARCHAR(50) PRIMARY KEY,
                    patient_id INTEGER,
                    amount INTEGER,
                    status VARCHAR(20),
                    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
        conn.commit()


# 3. Kafka configuration
config = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "hospital-analytics-group",
    "auto.offset.reset": "earliest",
}
consumer = Consumer(config)
consumer.subscribe(["orders"])

setup_db()
print("Listening for appointment events and writing to PostgreSQL...")
print("-" * 60)

try:
    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(f"Consumer error: {message.error()}")
            continue

        # Parse the event
        event = json.loads(message.value().decode("utf-8"))

        # Write to PostgreSQL
        try:
            with psycopg2.connect(**db_config) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO realtime_appointments (event_id, patient_id, amount, status)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (event_id) DO NOTHING;
                    """,
                        (
                            event["event_id"],
                            event["patient_id"],
                            event["amount"],
                            event["status"],
                        ),
                    )
                conn.commit()
            print(
                f"✅ Saved event {event['event_id']} to PostgreSQL | Patient: {event['patient_id']}"
            )
        except Exception as e:
            print(f"❌ Failed to save event {event['event_id']}: {e}")

except KeyboardInterrupt:
    print("\nStopping consumer...")
finally:
    consumer.close()
