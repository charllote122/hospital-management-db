-- =====================================================================
-- TRIGGERS AND AUTOMATION
-- =====================================================================

-- ---------------------------------------------------------------------
-- TRIGGER 1: AUDIT PAYMENT AMOUNT CHANGES
-- ---------------------------------------------------------------------

-- 1. Create the Audit Table
-- This table will store the history of payment changes.
CREATE TABLE IF NOT EXISTS payment_audit (
    audit_id SERIAL PRIMARY KEY,
    payment_id INTEGER,
    old_amount NUMERIC(10,2),
    new_amount NUMERIC(10,2),
    changed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Trigger Function
-- Trigger functions must return TRIGGER, not a standard data type.
CREATE OR REPLACE FUNCTION audit_payment_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Only log if the amount actually changed (IS DISTINCT FROM handles NULLs safely)
    IF OLD.amount IS DISTINCT FROM NEW.amount THEN
        INSERT INTO payment_audit (
            payment_id,
            old_amount,
            new_amount
        )
        VALUES (
            OLD.payment_id,
            OLD.amount,
            NEW.amount
        );
    END IF;
    
    -- For AFTER triggers, the return value is ignored, but we return NEW out of convention
    RETURN NEW;
END;
$$;

-- 3. Attach the Trigger to the Table
CREATE TRIGGER payment_update_audit_trigger
AFTER UPDATE ON payments
FOR EACH ROW
EXECUTE FUNCTION audit_payment_changes();

-- Test: Update the payment amount and check the audit table
-- UPDATE payments SET amount = 2500.00 WHERE payment_id = 1;
-- SELECT * FROM payment_audit;


-- ---------------------------------------------------------------------
-- TRIGGER 2: CLEAN PATIENT NAMES (BEFORE INSERT)
-- ---------------------------------------------------------------------

-- 1. Create the Trigger Function
CREATE OR REPLACE FUNCTION trim_patient_name()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Remove leading and trailing spaces from the new data
    NEW.first_name := TRIM(NEW.first_name);
    NEW.last_name := TRIM(NEW.last_name);
    
    -- Check if the name is empty after trimming and reject it
    IF NEW.first_name = '' OR NEW.last_name = '' THEN
        RAISE EXCEPTION 'Patient name cannot be empty';
    END IF;

    -- Return the modified row so PostgreSQL saves the cleaned version
    RETURN NEW;
END;
$$;

-- 2. Attach the Trigger to the Table
CREATE TRIGGER trim_patient_name_trigger
BEFORE INSERT OR UPDATE ON patients
FOR EACH ROW
EXECUTE FUNCTION trim_patient_name();

-- Test: Insert a messy name and see it get cleaned
-- INSERT INTO patients (first_name, last_name, date_of_birth) VALUES ('   John   ', '   Doe   ', '1985-05-20');
-- SELECT first_name, last_name FROM patients WHERE first_name = 'John';


-- ---------------------------------------------------------------------
-- TRIGGER 3: ARCHIVE DELETED APPOINTMENTS (AFTER DELETE)
-- ---------------------------------------------------------------------

-- 1. Create the Archive Table
CREATE TABLE IF NOT EXISTS deleted_appointments (
    appointment_id INTEGER,
    patient_id INTEGER,
    doctor_id INTEGER,
    scheduled_at TIMESTAMP,
    deleted_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Trigger Function
CREATE OR REPLACE FUNCTION archive_deleted_appointment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Insert the OLD row data into the archive table
    INSERT INTO deleted_appointments (
        appointment_id, patient_id, doctor_id, scheduled_at
    )
    VALUES (
        OLD.appointment_id, OLD.patient_id, OLD.doctor_id, OLD.scheduled_at
    );
    RETURN OLD;
END;
$$;

-- 3. Attach the Trigger to the Table
CREATE TRIGGER archive_appointment_delete_trigger
AFTER DELETE ON appointments
FOR EACH ROW
EXECUTE FUNCTION archive_deleted_appointment();

-- Test: Delete an appointment and check the archive
-- INSERT INTO appointments (patient_id, doctor_id, scheduled_at) VALUES (2, 1, '2026-11-16 10:00:00');
-- DELETE FROM appointments WHERE appointment_id = 2;
-- SELECT * FROM deleted_appointments;