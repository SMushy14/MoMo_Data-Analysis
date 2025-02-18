CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    transaction_type TEXT,
    amount INTEGER,
    sender_receiver TEXT,
    new_balance INTEGER,
    transaction_id TEXT
);
