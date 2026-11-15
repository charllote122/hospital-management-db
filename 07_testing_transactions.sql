-- ==========================================
-- HOW TO TEST TRANSACTIONS & CONCURRENCY
-- ==========================================

-- Test 1: Commit a successful transfer
BEGIN;
UPDATE accounts SET balance = balance - 5000 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 5000 WHERE account_id = 2;
COMMIT;

-- Test 2: Rollback a failed transfer
BEGIN;
UPDATE accounts SET balance = balance - 5000 WHERE account_id = 1;
ROLLBACK; -- Undoes the update above

-- Test 3: Using the PL/pgSQL Function
SELECT transfer_money(1, 2, 2000); 
-- Should return 'Transfer successful'

-- Test 4: Trying to break the function
SELECT transfer_money(1, 2, 999999); 
-- Should return ERROR: Insufficient funds

-- Test 5: Concurrency (Run this in TWO separate terminal tabs)
-- Terminal A:
BEGIN;
SELECT * FROM doctors WHERE doctor_id = 1 FOR UPDATE;
-- (Leave it hanging, do not commit yet)

-- Terminal B:
BEGIN;
SELECT * FROM doctors WHERE doctor_id = 1 FOR UPDATE;
-- (This will freeze until Terminal A types COMMIT;)