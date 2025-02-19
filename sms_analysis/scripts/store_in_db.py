import sqlite3
import csv
import os

# Define the database file path
db_file = os.path.join(os.path.dirname(__file__), "transactions.db")

# Check if the database file exists; if not, create it
if not os.path.exists(db_file):
    open(db_file, 'w').close()  # Create an empty file if it doesn't exist

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the transactions table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    transaction_type TEXT,
    amount INTEGER,
    sender_receiver TEXT,
    new_balance INTEGER,
    transaction_id TEXT
)
""")

# Insert data from CSV into database
csv_file = os.path.join(os.path.dirname(__file__), "../data/parsed_data.csv")
with open(csv_file, "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        cursor.execute("INSERT INTO transactions (date, transaction_type, amount, sender_receiver, new_balance, transaction_id) VALUES (?, ?, ?, ?, ?, ?)", row)

conn.commit()
conn.close()

print("Data successfully stored in the database.")
