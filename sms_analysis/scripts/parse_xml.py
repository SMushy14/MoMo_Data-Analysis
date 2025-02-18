import csv
import xml.etree.ElementTree as ET  # Import the XML parsing library

# Define file paths
xml_file_path = "/home/pamdacode/MoMo_Data-Analysis/sms_analysis/data/modified_sms_v2.xml"
csv_file_path = "/home/pamdacode/MoMo_Data-Analysis/sms_analysis/data/parsed_sms.csv"

# Parse the XML file
tree = ET.parse(xml_file_path)  # Load the XML file
root = tree.getroot()  # Get the root element

# Open the CSV file properly within a "with open" block
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)

    # Write the CSV header (Fixed missing comma)
    writer.writerow(["Date", "Transaction Type", "Amount", "Sender_Receiver", "New_Balance", "Transaction ID"])

    # Iterate over XML messages and extract transaction details
    for message in root.findall(".//message"):
        text_element = message.find("text")  # Get the SMS text element

        if text_element is not None and text_element.text:
            text = text_element.text
            parts = text.split("\n")  # Split SMS content into lines

            # Extract transaction details (handling missing fields safely)
            date = message.get("date", "N/A")
            transaction_type = parts[0] if len(parts) > 0 else "N/A"
            amount = parts[1].split("Amount: ")[1] if len(parts) > 1 and "Amount: " in parts[1] else "N/A"
            sender_receiver = parts[2].split("Sender_Receiver: ")[1] if len(parts) > 2 and "Sender_Receiver: " in parts[2] else "N/A"
            new_balance = parts[3].split("New_Balance: ")[1] if len(parts) > 3 and "New_Balance: " in parts[3] else "N/A"
            transaction_id = parts[0].split("TxId: ")[1] if "TxId: " in parts[0] else "N/A"

            # Write extracted data to the CSV file
            writer.writerow([date, transaction_type, amount, sender_receiver, new_balance, transaction_id])

print("XML parsing completed. Data saved in transactions.csv.")
