import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)

def get_transactions():
    db_file = os.path.join(os.path.dirname(__file__), "../db/sms_transactions.db")
    
    # Ensure the database file exists
    if not os.path.exists(db_file):
        print(f"Error: Database file '{db_file}' not found.")
        return []

    try:
        with sqlite3.connect(db_file) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions")
            data = cursor.fetchall()
            print("Fetched Transactions:", data)  # Debugging
            return data
    except sqlite3.Error as e:
        print("Database error:", e)
        return []

@app.route("/")
def home():
    transactions = get_transactions()
    return render_template("index.html", transactions=transactions)

if __name__ == "__main__":
    app.run(debug=True)
