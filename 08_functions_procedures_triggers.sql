-- =====================================================================
-- FUNCTIONS AND PROCEDURES
-- =====================================================================

-- 1. FUNCTION: Calculate Total Payments for a Patient
-- A function returns a value. Here, we calculate the total amount a patient 
-- has paid by joining the payments and appointments tables.
CREATE OR REPLACE FUNCTION get_patient_total_payments(
    p_patient_id INTEGER
)
RETURNS NUMERIC
LANGUAGE plpgsql
AS $$
DECLARE
    v_total NUMERIC;
BEGIN
    -- COALESCE handles cases where the patient has no payments yet (returns 0 instead of NULL)
    SELECT COALESCE(SUM(amount), 0)
    INTO v_total
    FROM payments p
    JOIN appointments a ON p.appointment_id = a.appointment_id
    WHERE a.patient_id = p_patient_id;

    RETURN v_total;
END;
$$;

-- Test the function (Assuming patient 1 has a payment)
-- SELECT get_patient_total_payments(1);


-- 2. PROCEDURE: Update Appointment Status
-- A procedure performs an action (workflow) and is called using CALL. 
-- It doesn't return a value like a function does.
CREATE OR REPLACE PROCEDURE update_appointment_status(
    p_appointment_id INTEGER,
    p_status VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Validation: Ensure the status is one of our allowed values
    IF p_status NOT IN ('scheduled', 'completed', 'cancelled', 'no_show') THEN
        RAISE EXCEPTION 'Invalid appointment status';
    END IF;

    -- Perform the update
    UPDATE appointments
    SET status = p_status
    WHERE appointment_id = p_appointment_id;

    -- Safety check: Did we actually update anything? 
    -- FOUND is a special PL/pgSQL variable that is TRUE if the last query affected rows.
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Appointment not found';
    END IF;
END;
$$;

-- Test the procedure
-- CALL update_appointment_status(1, 'completed');
-- CALL update_appointment_status(1, 'maybe'); -- This will fail with an error