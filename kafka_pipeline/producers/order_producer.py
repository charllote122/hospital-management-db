import json
import time
import random
from confluent_kafka import Producer

# 1. Configure the producer
config = {"bootstrap.servers": "localhost:9092"}
producer = Producer(config)


# 2. Delivery callback
def delivery_report(error, message):
    if error is not None:
        print(f"Delivery failed: {error}")
    else:
        print(
            f"✅ Delivered to partition {message.partition()} at offset {message.offset()}"
        )


# 3. Send 5 fake hospital appointment events
print("Sending 5 appointment events to Kafka...")
for i in range(1, 6):
    event = {
        "event_id": f"evt-{i:03d}",
        "event_type": "appointment_created",
        "patient_id": random.randint(1, 10),
        "doctor_id": random.randint(1, 3),
        "amount": random.randint(1000, 5000),
        "status": "scheduled",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    producer.produce(
        topic="orders",
        key=str(event["patient_id"]),
        value=json.dumps(event).encode("utf-8"),
        callback=delivery_report,
    )
    time.sleep(0.5)

# Wait for all messages to be delivered
producer.flush()
print("All events sent.")
