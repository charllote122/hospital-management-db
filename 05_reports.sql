-- Report: Appointments per Doctor
CREATE OR REPLACE VIEW v_appointments_per_doctor AS
SELECT
    d.doctor_id,
    d.first_name || ' ' || d.last_name AS doctor_name,
    dep.name AS department,
    COUNT(a.appointment_id) AS total_appointments,
    COUNT(*) FILTER (WHERE a.status = 'completed') AS completed,
    COUNT(*) FILTER (WHERE a.status = 'cancelled') AS cancelled,
    COUNT(*) FILTER (WHERE a.status = 'no_show')   AS no_shows
FROM doctors d
JOIN departments dep ON dep.department_id = d.department_id
LEFT JOIN appointments a ON a.doctor_id = d.doctor_id
GROUP BY d.doctor_id, d.first_name, d.last_name, dep.name;

-- Materialized View: Monthly Revenue
CREATE MATERIALIZED VIEW mv_monthly_revenue AS
SELECT
    date_trunc('month', paid_at)::DATE AS month,
    COUNT(DISTINCT appointment_id)     AS paying_appointments,
    SUM(amount)                        AS revenue
FROM payments
GROUP BY date_trunc('month', paid_at);

CREATE UNIQUE INDEX mv_monthly_revenue_month_idx ON mv_monthly_revenue(month);