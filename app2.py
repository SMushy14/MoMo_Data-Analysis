from flask import Flask, render_template_string
import sqlite3

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Transaction Records</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { width: 80%; border-collapse: collapse; margin: 20px auto; }
        th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
    </style>
</head>
<body>
    <h2 style="text-align: center;">Transaction Records</h2>
    <table>
        <tr>
            <th>Transaction ID</th>
            <th>Amount (RWF)</th>
            <th>Date & Time</th>
            <th>Transaction Type</th>
        </tr>
        {% for transaction in transactions %}
        <tr>
            <td>{{ transaction[0] }}</td>
            <td>{{ transaction[1] }}</td>
            <td>{{ transaction[2] }}</td>
            <td>{{ transaction[3] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def display_transactions():
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()
    cursor.execute("SELECT transaction_id, amount, date_time, transaction_type FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return render_template_string(template, transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
