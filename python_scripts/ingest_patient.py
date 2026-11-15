import os
import json
import psycopg
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

# 1. Simulate receiving a JSON payload from an external API
incoming_api_payload = {
    "patient_name": "Samuel Kipchoge",
    "contact": {"email": "samuel@example.com", "phone": "0711223344"},
    "age": 29,
    "allergies": ["Aspirin"],
    "insurance": {"provider": "Jubilee", "status": "active"},
}

# Convert Python dictionary to a JSON string
json_string = json.dumps(incoming_api_payload)

# 2. Connect to PostgreSQL
try:
    with psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    ) as connection:

        with connection.cursor() as cursor:
            # 3. Insert the JSON string into the JSONB column
            # We use %s placeholders to prevent SQL injection!
            sql = """
                INSERT INTO raw_api_patients (source_name, payload)
                VALUES (%s, %s::jsonb)
            """

            cursor.execute(sql, ("python_api", json_string))
            print("✅ Payload successfully inserted into PostgreSQL!")

except Exception as e:
    print("❌ Error connecting to database:", e)
