-- Insert Departments
INSERT INTO departments (name, location) VALUES ('Cardiology', 'Block A');

-- Insert Doctors
INSERT INTO doctors (first_name, last_name, specialty, department_id) 
VALUES ('Alice', 'Ngugi', 'Cardiologist', 1);

-- Insert Patients
INSERT INTO patients (first_name, last_name, date_of_birth, gender) 
VALUES ('Mary', 'Wanjiru', '1990-04-12', 'F');

-- Insert Appointments
INSERT INTO appointments (patient_id, doctor_id, scheduled_at, duration_min) 
VALUES (1, 1, '2026-11-15 09:00:00', 30);

-- Insert Medicines
INSERT INTO medicines (name, price) VALUES ('Paracetamol', 150.00), ('Amoxicillin', 450.00);

-- Insert Prescriptions
INSERT INTO prescriptions (appointment_id, notes) VALUES (1, 'Take with food.');

-- Insert Prescription Items
INSERT INTO prescription_items (prescription_id, medicine_id, quantity, dosage) 
VALUES 
(1, 1, 10, '1 tablet every 6 hours'),
(1, 2, 14, '1 capsule every 12 hours');

-- Insert Payments
INSERT INTO payments (appointment_id, amount, method) 
VALUES (1, 1500.00, 'card');