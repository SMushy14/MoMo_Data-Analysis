import sqlite3
import xml.etree.ElementTree as ET

def parse_uploaded_xml(file_path):
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id TEXT PRIMARY KEY,
        amount REAL,
        date_time TEXT,
        transaction_type TEXT
    )
    """)

    tree = ET.parse(file_path)
    root = tree.getroot()

    for transaction in root.findall(".//Transaction"):
        transaction_id = transaction.find("TransactionID").text
        amount = float(transaction.find("Amount").text)
        date_time = transaction.find("DateTime").text
        transaction_type = transaction.find("TransactionType").text

        cursor.execute("""
        INSERT OR IGNORE INTO transactions (transaction_id, amount, date_time, transaction_type)
        VALUES (?, ?, ?, ?)
        """, (transaction_id, amount, date_time, transaction_type))

        print(f"Inserted: {transaction_id} - {amount} - {date_time} - {transaction_type}")

    conn.commit()
    conn.close()
