CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL
);


CREATE TABLE IF NOT EXISTS bank_settlements (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    settlement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);


CRATE TABLE IF NOT EXITS payments (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);


-- ============================
-- ORDERS TABLE
-- ============================
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT,
    customer_email TEXT,
    order_total_cents INT,
    currency TEXT,
    is_test INT,
    created_at TIMESTAMP
);

-- ============================
-- PAYMENTS TABLE
-- ============================
CREATE TABLE IF NOT EXISTS payments (
    payment_id TEXT PRIMARY KEY,
    order_id TEXT NULL,
    attempt_no INT,
    provider TEXT,
    provider_ref TEXT,
    status TEXT CHECK (status IN ('SUCCESS', 'FAILED', 'PENDING')),
    amount_cents INT,
    attempted_at TIMESTAMP,
    
    CONSTRAINT fk_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE SET NULL
);

-- ============================
-- BANK SETTLEMENTS TABLE
-- ============================
CREATE TABLE IF NOT EXISTS bank_settlements (
    settlement_id TEXT PRIMARY KEY,
    payment_id TEXT NULL,
    provider_ref TEXT NULL,
    status TEXT CHECK (status IN ('SETTLED')),
    settled_amount_cents INT,
    currency TEXT,
    settled_at TIMESTAMP,
    
    CONSTRAINT fk_settlements_payment
        FOREIGN KEY (payment_id)
        REFERENCES payments(payment_id)
        ON DELETE SET NULL
);
