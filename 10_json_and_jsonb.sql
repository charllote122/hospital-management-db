-- =====================================================================
-- JSON AND JSONB IN POSTGRESQL
-- =====================================================================

-- 1. Create the Raw API Ingestion Table
-- We use JSONB because it is stored in a binary format, which is faster 
-- to query and supports indexing (unlike the plain JSON data type).
CREATE TABLE raw_api_patients (
    record_id BIGSERIAL PRIMARY KEY,
    source_name VARCHAR(100),
    payload JSONB NOT NULL,
    received_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- 2. Insert Semi-Structured JSON Data
-- Notice how the second patient has an array and a nested object.
INSERT INTO raw_api_patients (source_name, payload)
VALUES 
(
    'mobile_app',
    '{
        "patient_name": "Mary Wanjiru",
        "contact": {"email": "mary@example.com", "phone": "0712345678"},
        "age": 34,
        "allergies": ["Penicillin", "Peanuts"],
        "insurance": {"provider": "NHIF", "status": "active"}
    }'
),
(
    'web_portal',
    '{
        "patient_name": "John Doe",
        "contact": {"email": "john@example.com", "phone": "0787654321"},
        "age": 45,
        "allergies": ["None"],
        "insurance": {"provider": "AAR", "status": "expired"}
    }'
);

-- =====================================================================
-- QUERYING JSON DATA
-- =====================================================================

-- 3. Extract Data using Operators
-- -> returns JSON (good for arrays/objects)
-- ->> returns plain Text
-- We cast the age to INTEGER so it behaves like a normal column.
SELECT 
    payload ->> 'patient_name' AS name,
    payload -> 'contact' ->> 'email' AS email,
    (payload ->> 'age')::INTEGER AS age,
    payload -> 'insurance' ->> 'provider' AS insurance
FROM raw_api_patients;

-- 4. Query Arrays (Find specific items)
-- The ? operator checks if a JSON array contains a specific string.
SELECT payload ->> 'patient_name' AS name 
FROM raw_api_patients
WHERE payload -> 'allergies' ? 'Peanuts';

-- 5. Containment Filtering (@>)
-- The @> operator asks: "Does this JSONB document contain this specific chunk?"
SELECT payload ->> 'patient_name' AS name 
FROM raw_api_patients
WHERE payload @> '{"insurance": {"status": "active"}}';

-- 6. Expand Arrays into Rows (Data Engineering Technique)
-- CROSS JOIN LATERAL explodes the array so each item becomes its own row.
SELECT 
    payload ->> 'patient_name' AS name,
    allergy
FROM raw_api_patients
CROSS JOIN LATERAL jsonb_array_elements_text(payload -> 'allergies') AS allergy;

-- =====================================================================
-- UPDATING JSON DATA
-- =====================================================================

-- 7. Update Nested JSON Values (jsonb_set)
-- Let's say John renewed his insurance. We update the status from 'expired' to 'active'.
UPDATE raw_api_patients
SET payload = jsonb_set(
    payload, 
    '{insurance,status}', 
    '"active"'::JSONB
)
WHERE payload ->> 'patient_name' = 'John Doe';

-- Verify the change
SELECT payload -> 'insurance' ->> 'status' 
FROM raw_api_patients 
WHERE payload ->> 'patient_name' = 'John Doe';

-- =====================================================================
-- PERFORMANCE OPTIMIZATION
-- =====================================================================

-- 8. Create a GIN Index
-- GIN (Generalized Inverted Index) makes @>, ?, and other JSONB 
-- searches incredibly fast on large datasets.
CREATE INDEX idx_raw_patients_payload ON raw_api_patients USING GIN (payload);