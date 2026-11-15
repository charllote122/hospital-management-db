CREATE OR REPLACE VIEW v_appointment_details AS
SELECT
    a.appointment_id,
    a.scheduled_at,
    a.duration_min,
    a.status,
    p.first_name || ' ' || p.last_name AS patient_name,
    d.first_name || ' ' || d.last_name AS doctor_name,
    dep.name AS department,
    COALESCE(SUM(pay.amount), 0)::NUMERIC(10,2) AS total_paid
FROM appointments a
JOIN patients     p   ON p.patient_id  = a.patient_id
JOIN doctors      d   ON d.doctor_id   = a.doctor_id
JOIN departments  dep ON dep.department_id = d.department_id
LEFT JOIN payments pay ON pay.appointment_id = a.appointment_id
GROUP BY a.appointment_id, p.first_name, p.last_name,
         d.first_name, d.last_name, dep.name;