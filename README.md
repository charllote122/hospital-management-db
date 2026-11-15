# 🏥 Hospital Management System Database

A complete, production-ready PostgreSQL database architecture for a hospital management system, complete with a Python ETL ingestion pipeline.

This project demonstrates advanced database design, data integrity constraints, performance optimization, and Python-to-PostgreSQL integration.

## 🚀 Features
- **Relational Design:** 10+ normalized tables with strict Primary/Foreign Key constraints.
- **Data Integrity:** Exclusion constraints to prevent doctors from being double-booked.
- **Automation:** PL/pgSQL functions for financial calculations and triggers for automatic payment auditing and data cleaning.
- **Transactions:** Concurrency control (row-level locking) to prevent deadlocks during financial transfers.
- **Reporting:** Views and Materialized Views for real-time and cached analytical dashboards.
- **Semi-Structured Data:** JSONB raw ingestion table with GIN indexing for API payloads.
- **Performance:** B-Tree indexing and `EXPLAIN ANALYZE` optimization demonstrated on 100,000+ rows.
- **Python ETL:** A Python script using `psycopg` to ingest JSON API payloads directly into PostgreSQL.

---

## 🛠️ Project Structure

```text
hospital-management-db/
│
├── 01_create_tables.sql          # Creates all 8 core tables and foreign keys
├── 02_insert_seed_data.sql       # Inserts sample hospitals, doctors, patients
├── 03_constraints.sql            # Adds the exclusion constraint (No Double-Booking)
├── 04_views.sql                  # Creates the appointment details view
├── 05_reports.sql                # Creates doctor reports and revenue materialized views
├── 06_transactions_and_functions.sql # Bank accounts and ACID transfer functions
├── 07_testing_transactions.sql   # Scripts to test concurrency and rollbacks
├── 08_functions_and_procedures.sql # Payment calculations and status updates
├── 09_triggers_and_automation.sql  # Audit logs, name trimming, and deletion archiving
├── 10_json_and_jsonb.sql         # JSONB ingestion tables and query techniques
├── 11_query_optimization.sql     # 100k row generation and index performance testing
│
├── python_scripts/               # Python ETL Integration
│   ├── ingest_patient.py         # Python script to push JSON to PostgreSQL
│   ├── .env                      # (Ignored in Git) Database credentials
│   └── .gitignore                # Prevents secrets from being pushed
│
└── README.md


## Relationships:
- **Departments** (1) ─── (N) **Doctors**
- **Patients** (1) ─── (N) **Appointments**
- **Doctors** (1) ─── (N) **Appointments**
- **Appointments** (1) ─── (0..1) **Prescriptions**
- **Prescriptions** (1) ─── (N) **Prescription_Items**
- **Medicines** (1) ─── (N) **Prescription_Items**
- **Appointments** (1) ─── (N) **Payments**

## Setup Instructions
Run the files in this exact order to build the database:
\i 01_create_tables.sql
\i 02_insert_seed_data.sql
\i 03_constraints.sql
\i 04_views.sql
\i 05_reports.sql
\i 08_functions_and_procedures.sql
\i 09_triggers_and_automation.sql
\i 10_json_and_jsonb.sql

## ER Diagram

```text
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

