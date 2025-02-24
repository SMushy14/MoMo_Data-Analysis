import sqlite3
import xml.etree.ElementTree as ET
import re
import matplotlib.pyplot as plt

def extract_transaction_details(text):
    """Extracts transaction details from SMS body."""
    transaction_id = re.search(r'TxId[:\s]*(\d+)', text)
    amount = re.search(r'(\d+)\s*RWF', text)
    date_time = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', text)
    
    # Determine transaction type
    if "received" in text or "deposit" in text:
        transaction_type = "Deposit"
    elif "transferred" in text:
        transaction_type = "Transfer"
    elif "payment" in text:
        transaction_type = "Payment"
    elif "purchased" in text or "airtime" in text or "bundle" in text:
        transaction_type = "Purchase"
    else:
        transaction_type = "Unknown"

    return {
        "transaction_id": transaction_id.group(1) if transaction_id else None,
        "amount": int(amount.group(1)) if amount else 0,
        "date_time": date_time.group(1) if date_time else None,
        "transaction_type": transaction_type
    }

def create_database():
    """Creates an SQLite database to store transactions."""
    conn = sqlite3.connect("parsed_data2.db")
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
    """Inserts transaction data into the SQLite database."""
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (transaction_id, amount, date_time, transaction_type)  
        VALUES (?, ?, ?, ?)
    ''', (data["transaction_id"], data["amount"], data["date_time"], data["transaction_type"]))
    conn.commit()
    conn.close()

def parse_xml_file():
    """Parses the XML file and extracts transaction details."""
    tree = ET.parse("modified_sms_v2.xml")
    root = tree.getroot()

    for sms in root.findall("sms"):
        body = sms.attrib.get("body", "")
        transaction_details = extract_transaction_details(body)
        if transaction_details["date_time"]:
            insert_transaction(transaction_details)

def generate_dashboard():
    """Generates a bar chart showing total spending per transaction type."""
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT transaction_type, SUM(amount) 
        FROM transactions 
        WHERE transaction_type != "Deposit" 
        GROUP BY transaction_type
    ''')
    
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No transactions found for dashboard visualization.")
        return

    transaction_types = [row[0] for row in data]
    amounts = [row[1] for row in data]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(transaction_types, amounts, color=['red', 'blue', 'green', 'orange'])
    plt.xlabel("Transaction Type")
    plt.ylabel("Total Amount Spent (RWF)")
    plt.title("Total Amount Spent on Different Transactions")
    plt.xticks(rotation=45)
    plt.show()

def main():
    create_database()
    parse_xml_file()
    print("modified sms v2 file parsing and storage completed.")
    generate_dashboard()

if __name__ == "__main__":
    main()
