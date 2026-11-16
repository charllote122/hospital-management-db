# 🏥 Hospital Management System

A complete, production-grade Data Engineering portfolio project demonstrating the entire modern data stack: **Relational Database Design, ETL, Orchestration, Distributed Processing, Real-Time Streaming, Lakehouse, Data Warehousing, and Analytics Engineering.**

## 🚀 Features

### 1. Relational Database Design (PostgreSQL)
- **10+ Normalized Tables** with strict Primary/Foreign Key constraints.
- **Data Integrity:** Exclusion constraints to prevent doctors from being double-booked.
- **ACID Transactions:** Row-level locking to prevent deadlocks during financial transfers.
- **Triggers & Functions:** Automatic payment auditing and data cleaning.
- **JSONB Ingestion:** GIN-indexed raw API payload storage.

### 2. Performance Optimization (PostgreSQL)
- **B-Tree Indexing:** Reduced query time from **28.9ms to 0.12ms** on 100,000+ rows (demonstrated with `EXPLAIN ANALYZE`).
- **Materialized Views** for cached analytical dashboards.

### 3. Python ETL Pipeline
- Modular `extract`, `transform`, `validate`, `load` scripts.
- Uses `psycopg2` / `psycopg` to ingest JSON API payloads.
- Rotating file logging and Pytest unit tests.
- Idempotent loading using `ON CONFLICT DO NOTHING`.

### 4. Orchestration (Apache Airflow + Docker)
- Dockerized Airflow running a DAG (`hospital_etl_pipeline`) with retries and error handling.
- Automates the Python ETL pipeline end-to-end.

### 5. Distributed Processing (PySpark)
- **Medallion Architecture:** Bronze (raw), Silver (cleaned), Gold (aggregated) layers.
- Reads CSV, enforces schemas, calculates revenue, and writes **Parquet** files.
- Writes Gold data to PostgreSQL via **JDBC**.

### 6. Real-Time Streaming (Apache Kafka)
- Python **Producer** publishing appointment events.
- Python **Consumer** reading events and writing to PostgreSQL in real-time.
- Demonstrates topics, partitions, and offsets.

### 7. Data Lakehouse (Delta Lake)
- Creates **Delta Tables** on top of Parquet storage.
- **ACID Transactions:** In-place updates without rewriting the entire table.
- **Time Travel:** Query the table as it existed before an update.

### 8. Data Warehousing (Dimensional Modelling)
- **Star Schema:** Fact and Dimension tables in a dedicated `warehouse` schema.
- **Date Dimension** generated with `GENERATE_SERIES`.
- Analytical SQL queries (Revenue by Category, City, and Month).

### 9. Analytics Engineering (dbt)
- **dbt Project:** Modular SQL models for `dim_customer`, `fact_sales`, and `revenue_by_category`.
- Connected to PostgreSQL with `profiles.yml`.
- Builds views/tables inside the `dbt_warehouse` schema.

---

## 🛠️ Project Structure

```text
hospital-management-db/
│
├── 01_create_tables.sql              # Core tables and foreign keys
├── 02_insert_seed_data.sql           # Seed data
├── 03_constraints.sql                # Exclusion constraint (No Double-Booking)
├── 04_views.sql                      # Appointment details view
├── 05_reports.sql                    # Doctor reports and revenue views
├── 06_transactions_and_functions.sql # Bank accounts and ACID transfer functions
├── 07_testing_transactions.sql       # Concurrency and rollback tests
├── 08_functions_and_procedures.sql   # Payment calculations and status updates
├── 09_triggers_and_automation.sql    # Audit logs, name trimming, deletion archiving
├── 10_json_and_jsonb.sql             # JSONB ingestion and querying
├── 11_query_optimization.sql         # 100k row generation and indexing
│
├── python_scripts/                   # Python ETL
│   ├── main_etl.py
│   ├── ingest_patient.py
│   ├── config/settings.py
│   ├── extract/extract_csv.py
│   ├── transform/transform_orders.py
│   ├── validation/validate_orders.py
│   ├── load/load_orders.py
│   ├── tests/test_transform.py
│   └── .env                          # (Ignored in Git) DB credentials
│
├── dags/                             # Airflow DAGs
│   └── hospital_etl_dag.py
│
├── spark_pipeline/                   # PySpark Medallion Architecture
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── extraction/read_data.py
│   │   ├── transformation/cleaning.py
│   │   ├── validation/quality_checks.py
│   │   ├── loading/write_data.py
│   │   └── lakehouse.py              # Delta Lake ACID + Time Travel
│   ├── data/bronze/ silver/ gold/
│   └── jars/postgresql-42.7.14.jar
│
├── kafka_pipeline/                   # Real-Time Streaming
│   ├── docker-compose.yml
│   ├── producers/order_producer.py
│   ├── consumers/order_consumer.py
│   └── spark_streaming.py
│
├── hospital_dbt/                     # dbt Analytics Engineering
│   ├── models/
│   │   ├── dim_customer.sql
│   │   ├── fact_sales.sql
│   │   └── revenue_by_category.sql
│   └── dbt_project.yml
│
├── docker-compose.yaml               # Airflow
└── README.md


🗄️ Database Schema & Relationships
Departments (1) ─── (N) Doctors

Patients (1) ─── (N) Appointments

Doctors (1) ─── (N) Appointments

Appointments (1) ─── (0..1) Prescriptions

Prescriptions (1) ─── (N) Prescription_Items

Medicines (1) ─── (N) Prescription_Items

Appointments (1) ─── (N) Payments

⚙️ Setup Instructions
1. PostgreSQL Database
Run the SQL files in order:
\i 01_create_tables.sql
\i 02_insert_seed_data.sql
\i 03_constraints.sql
\i 04_views.sql
\i 05_reports.sql
\i 08_functions_and_procedures.sql
\i 09_triggers_and_automation.sql
\i 10_json_and_jsonb.sql
\i 11_query_optimization.sql

2. Python ETL

cd python_scripts
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
python main_etl.py

3. Airflow (Docker)

docker compose up airflow-init
docker compose up -d
# Open http://localhost:8080 (admin/admin)

4. PySpark
python spark_pipeline/src/main.py

5. Kafka
cd kafka_pipeline
docker compose up -d
# Terminal 1: python consumers/order_consumer.py
# Terminal 2: python producers/order_producer.py

6. Delta Lake
python spark_pipeline/src/lakehouse.py

7. dbt
cd hospital_dbt
dbt run

📊 ER Diagram
┌────────────────┐          ┌────────────────┐
│  departments   │1        N│    doctors     │
│────────────────│──────────│────────────────│
│ department_id  │          │ doctor_id (PK) │
│ name           │          │ department_id  │
└────────────────┘          └───────┬────────┘
                                    │ 1
                                    │
                                    │ N
┌────────────────┐  1      N ┌──────┴─────────────┐ 1      0..1 ┌────────────────┐
│   patients     │───────────│    appointments    │──────────────│  prescriptions │
│────────────────│           │────────────────────│              │────────────────│
│ patient_id (PK)│           │ appointment_id (PK)│              │ prescription_id│
│ name, dob...   │           │ patient_id (FK)    │              │ appointment_id │
└────────────────┘           │ doctor_id  (FK)    │              │ issued_at      │
                             │ scheduled_at       │              └───────┬────────┘
                             │ duration_min       │                      │ 1
                             │ status             │                      │
                             └────┬──────────┬────┘                      │ N
                                  │ 1        │ 1        ┌─────────────────┴────────┐
                                  │          │          │  prescription_items      │
                                  │          │          │──────────────────────────│
                                  │          │          │ prescription_item_id (PK)│
                                  │          │          │ prescription_id (FK)     │
                                  │          │          │ medicine_id (FK)         │
                                  │          │          │ quantity, dosage         │
                                  │          │          └────────────┬─────────────┘
                                  │          │                       │ N
                                  │          │                       │ 1
                                  │          │          ┌────────────┴─────────────┐
                                  │          │          │       medicines          │
                                  │          │          │──────────────────────────│
                                  │          │          │ medicine_id (PK)         │
                                  │          │          │ name, unit, price        │
                                  │          │          └──────────────────────────┘
                                  │ N        │
                            ┌─────┴────────┐ │
                            │   payments   │ │
                            │──────────────│ │
                            │ payment_id PK│ │
                            │ appointment_id (FK) │
                            │ amount, method, paid_at │
                            └──────────────┘


🏆 Skills Demonstrated
Category	Technologies
Databases	PostgreSQL, SQL, Star Schema, Dimensional Modelling
Programming	Python, Pandas, PySpark
Orchestration	Apache Airflow, Docker
Streaming	Apache Kafka
Lakehouse	Delta Lake (ACID, Time Travel)
Analytics Engineering	dbt
Testing	Pytest
Version Control	Git, GitHub
