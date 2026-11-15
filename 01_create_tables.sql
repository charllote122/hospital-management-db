-- 1. PATIENTS
CREATE TABLE patients (
    patient_id     SERIAL PRIMARY KEY,
    first_name     VARCHAR(100) NOT NULL,
    last_name      VARCHAR(100) NOT NULL,
    date_of_birth  DATE         NOT NULL,
    gender         VARCHAR(10)  CHECK (gender IN ('M','F','Other')),
    phone          VARCHAR(20)  UNIQUE,
    email          VARCHAR(255) UNIQUE,
    address        TEXT,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- 2. DEPARTMENTS
CREATE TABLE departments (
    department_id   SERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL UNIQUE,
    location        VARCHAR(100)
);

-- 3. DOCTORS
CREATE TABLE doctors (
    doctor_id       SERIAL PRIMARY KEY,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    specialty       VARCHAR(100),
    phone           VARCHAR(20)  UNIQUE,
    email           VARCHAR(255) UNIQUE,
    department_id   INT NOT NULL REFERENCES departments(department_id) ON DELETE RESTRICT
);

-- 4. APPOINTMENTS
CREATE TABLE appointments (
    appointment_id  SERIAL PRIMARY KEY,
    patient_id      INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    doctor_id       INT NOT NULL REFERENCES doctors(doctor_id) ON DELETE RESTRICT,
    scheduled_at    TIMESTAMP NOT NULL,
    duration_min    INT NOT NULL DEFAULT 30 CHECK (duration_min > 0),
    status          VARCHAR(20) NOT NULL DEFAULT 'scheduled' CHECK (status IN ('scheduled','completed','cancelled','no_show')),
    ends_at         TIMESTAMP GENERATED ALWAYS AS (scheduled_at + (duration_min * INTERVAL '1 minute')) STORED
);

-- 5. MEDICINES
CREATE TABLE medicines (
    medicine_id     SERIAL PRIMARY KEY,
    name            VARCHAR(150) NOT NULL,
    manufacturer    VARCHAR(150),
    unit            VARCHAR(30),
    price           NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (price >= 0)
);

-- 6. PRESCRIPTIONS
CREATE TABLE prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    appointment_id  INT NOT NULL UNIQUE REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    issued_at       TIMESTAMP NOT NULL DEFAULT now(),
    notes           TEXT
);

-- 7. PRESCRIPTION ITEMS
CREATE TABLE prescription_items (
    prescription_item_id SERIAL PRIMARY KEY,
    prescription_id      INT NOT NULL REFERENCES prescriptions(prescription_id) ON DELETE CASCADE,
    medicine_id          INT NOT NULL REFERENCES medicines(medicine_id) ON DELETE RESTRICT,
    quantity             INT NOT NULL CHECK (quantity > 0),
    dosage               VARCHAR(100),
    UNIQUE (prescription_id, medicine_id)
);

-- 8. PAYMENTS
CREATE TABLE payments (
    payment_id     SERIAL PRIMARY KEY,
    appointment_id INT NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    amount         NUMERIC(10,2) NOT NULL CHECK (amount > 0),
    method         VARCHAR(20) CHECK (method IN ('cash','card','insurance','transfer')),
    paid_at        TIMESTAMP NOT NULL DEFAULT now()
);