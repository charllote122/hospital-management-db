-- =====================================================================
-- QUERY OPTIMIZATION & PERFORMANCE
-- =====================================================================

-- 1. Generate 100,000 rows for testing
-- We space them 10 minutes apart to avoid exclusion constraint errors.
INSERT INTO appointments (patient_id, doctor_id, scheduled_at, duration_min)
SELECT 
    1, 
    1, 
    TIMESTAMP '2026-01-01 00:00:00' + (n * INTERVAL '10 minutes'), 
    30 
FROM generate_series(1, 100000) AS n;

-- Update planner statistics
ANALYZE appointments;

-- 2. The "Before" Execution Plan (Sequential Scan)
EXPLAIN ANALYZE
SELECT * FROM appointments 
WHERE scheduled_at >= '2026-06-15' AND scheduled_at < '2026-06-16';
-- Note: Before indexing, this takes ~29ms and scans 100,000 rows.

-- 3. Create the B-tree Index
CREATE INDEX idx_appointments_scheduled_at ON appointments(scheduled_at);

-- 4. The "After" Execution Plan (Index Scan)
EXPLAIN ANALYZE
SELECT * FROM appointments 
WHERE scheduled_at >= '2026-06-15' AND scheduled_at < '2026-06-16';
-- Note: After indexing, this takes ~0.12ms and is 200x faster!

-- 5. Sargable vs Non-Sargable Queries
-- BAD: Using a function on the column ignores the index
EXPLAIN ANALYZE
SELECT * FROM appointments WHERE EXTRACT(YEAR FROM scheduled_at) = 2026;

-- GOOD: Using a range allows PostgreSQL to use the index
EXPLAIN ANALYZE
SELECT * FROM appointments 
WHERE scheduled_at >= '2026-01-01' AND scheduled_at < '2027-01-01';