-- ==========================================
-- TRANSACTIONS, ACID & CONCURRENCY
-- ==========================================

-- 1. Create Accounts Table
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    account_holder VARCHAR(100),
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO accounts (account_holder, balance)
VALUES 
('Mary Wanjiru', 20000), 
('Alice Ngugi', 10000);


-- 2. Create Inventory Table (for Intermediate task)
CREATE TABLE inventory (
    medicine_id INT PRIMARY KEY REFERENCES medicines(medicine_id),
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0)
);

INSERT INTO inventory (medicine_id, stock_quantity) VALUES (1, 10), (2, 5);


-- 3. Create the Transfer Money Function (Advanced task)
CREATE OR REPLACE FUNCTION transfer_money(
    p_from_account INT,
    p_to_account INT,
    p_amount NUMERIC
)
RETURNS TEXT
LANGUAGE plpgsql
AS $$
DECLARE
    v_from_balance NUMERIC(12, 2);
BEGIN
    IF p_amount IS NULL OR p_amount <= 0 THEN
        RAISE EXCEPTION 'Transfer amount must be positive';
    END IF;

    IF p_from_account = p_to_account THEN
        RAISE EXCEPTION 'Source and destination must differ';
    END IF;

    -- Lock both accounts in a consistent order to prevent deadlocks
    PERFORM account_id
    FROM accounts
    WHERE account_id IN (p_from_account, p_to_account)
    ORDER BY account_id
    FOR UPDATE;

    -- Verify that both accounts exist
    IF (
        SELECT COUNT(*)
        FROM accounts
        WHERE account_id IN (p_from_account, p_to_account)
    ) <> 2 THEN
        RAISE EXCEPTION 'One or both accounts do not exist';
    END IF;

    SELECT balance INTO v_from_balance FROM accounts WHERE account_id = p_from_account;

    IF v_from_balance < p_amount THEN
        RAISE EXCEPTION 'Insufficient funds';
    END IF;

    UPDATE accounts SET balance = balance - p_amount WHERE account_id = p_from_account;
    UPDATE accounts SET balance = balance + p_amount WHERE account_id = p_to_account;

    RETURN 'Transfer successful';

END;
$$;