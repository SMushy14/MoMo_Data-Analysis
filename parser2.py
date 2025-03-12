import sqlite3
import xml.etree.ElementTree as ET
import re  # Import regex for extracting data


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

    for sms in root.findall(".//sms"):
        body = sms.get("body")  # Get the SMS message content

        if body:
            # Detect different transaction types based on message patterns
            receive_match = re.search(r"You have received (\d{1,3}(?:,\d{3})*) RWF.*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?Financial Transaction Id: (\d+)", body)
            payment_match = re.search(r"TxId:\s*(\d+).*?Your payment of (\d{1,3}(?:,\d{3})*) RWF.*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
            transfer_match = re.search(r"(\d{1,3}(?:,\d{3})*) RWF transferred to .*?at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
            bank_deposit_match = re.search(r"A bank deposit of (\d{1,3}(?:,\d{3})*) RWF has been added to your mobile account at (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)

            if receive_match:
               amount=float(receive_match.group(1).replace(",", ""))  # Remove commas for thousands
               date_time=receive_match.group(2)
               transaction_id=receive_match.group(3)
               transaction_type="Received"
            
            elif payment_match:
                 transaction_id=payment_match.group(1)
                 amount=float(payment_match.group(2).replace(",", ""))
                 date_time=payment_match.group(3)
                 transaction_type="Payment"
            
            elif transfer_match:
                 amount=float(transfer_match.group(1).replace(",", ""))
                 date_time=transfer_match.group(2)
                 transaction_id="None"
                 transaction_type="Transfer"
             
            elif bank_deposit_match:
                 amount=float(bank_deposit_match.group(1).replace(",", ""))
                 date_time=bank_deposit_match.group(2)
                 transaction_id="None"
                 transaction_type="Bank Deposit"
            
            else:
                transaction_type="Unknown"
                amount=0.0
                date_time="Unknown"
                transaction_id="None"

            # Insert into database
            cursor.execute("""
            INSERT OR IGNORE INTO transactions (transaction_id, amount, date_time, transaction_type)
            VALUES (?, ?, ?, ?)
            """, (transaction_id, amount, date_time, transaction_type))

            print(f"Inserted: {transaction_id} - {amount} - {date_time} - {transaction_type}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    xml_file_path="modified_sms_v2.xml"
    parse_uploaded_xml(xml_file_path)
