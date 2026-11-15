-- Enable the ability to mix text (doctor_id) and time ranges
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Add the exclusion constraint to prevent double-booking a doctor
ALTER TABLE appointments
ADD CONSTRAINT no_overlapping_appointments
EXCLUDE USING gist (
    doctor_id  WITH =,
    tsrange(scheduled_at, ends_at, '[)') WITH &&
)
WHERE (status <> 'cancelled');