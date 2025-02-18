import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """Parses the XML file and extracts SMS transaction details."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    transactions = []

    for sms in root.findall('sms'):
        body = sms.find('body').text if sms.find('body') is not None else ""

        # Extract transaction details using simple text parsing
        transaction = {
            "body": body,
            "type": categorize_transaction(body),
            "amount": extract_amount(body),
            "date": extract_date(body),
            "transaction_id": extract_transaction_id(body)
        }

        transactions.append(transaction)

    return transactions

def categorize_transaction(body):
    """Categorizes the transaction based on keywords in the message body."""
    if "received" in body.lower():
        return "Incoming Money"
    elif "payment" in body.lower():
        return "Payments to Code Holders"
    elif "withdrawn" in body.lower():
        return "Withdrawals from Agents"
    elif "bundle" in body.lower():
        return "Internet and Voice Bundle Purchases"
    else:
        return "Other"

def extract_amount(body):
    """Extracts transaction amount from the message body."""
    import re
    match = re.search(r"(\d+)\s*RWF", body)
    return int(match.group(1)) if match else None

def extract_date(body):
    """Extracts the transaction date from the message body."""
    import re
    match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", body)
    return match.group(1) if match else None

def extract_transaction_id(body):
    """Extracts the transaction ID from the message body."""
    import re
    match = re.search(r"TxId[: ]?(\d+)", body)
    return match.group(1) if match else None

# Example Usage
if __name__ == "__main__":
    xml_file_path = "modified_sms_v2.xml"  # Update this path as needed
    transactions = parse_xml(xml_file_path)
    for tx in transactions[:5]:  # Print first 5 transactions for verification
        print(tx)
