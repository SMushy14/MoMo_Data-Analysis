from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Transaction Records</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        table { width: 80%; border-collapse: collapse; margin: 20px auto; }
        th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }
        th { background-color: #f4f4f4; }
        .container { width: 80%; margin: auto; }
        .filter-form { margin-bottom: 20px; }
        .summary-card {
            display: inline-block;
            width: 30%;
            padding: 15px;
            margin: 10px;
            background: #f4f4f4;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #aaa;
        }
    </style>
</head>
<body>
    <h2>Transaction Records</h2>

    <!-- Filter Form -->
    <form class="filter-form" method="GET">
        <label for="transaction_type">Filter by Transaction Type:</label>
        <select name="transaction_type">
            <option value="">All</option>
            <option value="Deposit" {% if filter_type == 'Deposit' %}selected{% endif %}>Deposit</option>
            <option value="Withdrawal" {% if filter_type == 'Withdrawal' %}selected{% endif %}>Withdrawal</option>
            <option value="Payment" {% if filter_type == 'Payment' %}selected{% endif %}>Payment</option>
        </select>
        <button type="submit">Filter</button>
    </form>

    <!-- Summary Cards -->
    <div class="container">
        {% for type, total in summary.items() %}
            <div class="summary-card">
                <h3>{{ type }}</h3>
                <p><strong>{{ total }} RWF</strong></p>
            </div>
        {% endfor %}
    </div>

    <!-- Transactions Table -->
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

def get_transactions(transaction_type=None):
    """Fetch transactions from the database, optionally filtering by type."""
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()

    if transaction_type:
        cursor.execute("SELECT transaction_id, amount, date_time, transaction_type FROM transactions WHERE transaction_type = ?", (transaction_type,))
    else:
        cursor.execute("SELECT transaction_id, amount, date_time, transaction_type FROM transactions")
    
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_transaction_summary():
    """Calculate the total amount spent per transaction type."""
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT transaction_type, SUM(amount) FROM transactions GROUP BY transaction_type")
    summary = {row[0]: row[1] for row in cursor.fetchall()}
    
    conn.close()
    return summary

@app.route('/')
def display_transactions():
    filter_type = request.args.get('transaction_type')
    transactions = get_transactions(filter_type)
    summary = get_transaction_summary()
    
    return render_template_string(template, transactions=transactions, filter_type=filter_type, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
