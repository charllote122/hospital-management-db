# Hospital Management System Database

This project contains a fully normalized PostgreSQL database for a hospital, featuring advanced constraints (no double-booking) and analytical views.

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
1. `\i 01_create_tables.sql`
2. `\i 02_insert_seed_data.sql`
3. `\i 03_constraints.sql`
4. `\i 04_views.sql`
5. `\i 05_reports.sql`
6. `\i 06_transactions_and_functions.sql`
7. `\i 07_testing_transactions.sql`

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

                            