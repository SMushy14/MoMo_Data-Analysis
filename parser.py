import sqlite3
import xml.etree.ElementTree as ET
import re

def extract_transaction_details(text):
    transaction_id = re.search(r'TxId[:\s]*(\d+)', text)
    amount = re.search(r'(\d+) RWF', text)
    date_time = re.search(r'Date: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', text)
    transaction_type = "Unknown"

    if "received" in text:
        transaction_type = "Deposit"
    elif "withdrawn" in text:
        transaction_type = "Withdrawal"
    elif "payment" in text:
        transaction_type = "Payment"
    elif "purchased an internet bundle" in text:
        transaction_type = "Purchase"

    return {
        "transaction_id": transaction_id.group(1) if transaction_id else None,
        "amount": int(amount.group(1)) if amount else None,
        "date_time": date_time.group(1) if date_time else None,
        "transaction_type": transaction_type
    }

def create_database():
    conn = sqlite3.connect("parsed_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            amount INTEGER,
            date_time TEXT,
            transaction_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_transaction(data):
    conn = sqlite3.connect("parsed_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (transaction_id, amount, date_time, transaction_type)
        VALUES (?, ?, ?, ?)
    ''', (data["transaction_id"], data["amount"], data["date_time"], data["transaction_type"]))
    conn.commit()
    conn.close()

def parse_xml_file():
    tree = ET.parse("sample_data.xml")
    root = tree.getroot()

    for sms in root.findall("sms"):
        body = sms.find("body").text
        transaction_details = extract_transaction_details(body)
        if transaction_details["date_time"]:
            insert_transaction(transaction_details)

def main():
    create_database()
    parse_xml_file()
    print("Xml file parsing and storage completed.")

if __name__ == "__main__":
    main()
