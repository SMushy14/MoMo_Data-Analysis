from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_transaction_totals():
    conn = sqlite3.connect('parsed_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type='Deposit'")
    total_deposits = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type='Withdrawal'")
    total_withdrawals = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE transaction_type='Payment'")
    total_spent = cursor.fetchone()[0] or 0

    conn.close()

    return {
        'total_deposits': total_deposits,
        'total_withdrawals': total_withdrawals,
        'total_spent': total_spent
    }

@app.route('/')
def dashboard():
    totals = get_transaction_totals()
    return render_template('index.html', totals=totals)

html_template = """
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>MoMo Dashboard</title>
    <style>
        body {
            font-family: monospace;
            text-align: center;
            padding: 20px;
            background-color: #f6e4d2;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            border: 1px solid #142339;
            border-radius: 10px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: #142339;
        }
        h1 {
            color: #142339;
        }
        .amount {
            font-size: 24px;
            margin: 10px 0;
            text-align: left;
        }
        strong {
            color: #142339;
        }
    </style>
</head>
<body>
    <div class='container'>
        <h1>MoMo Dashboard</h1>
        <p class='amount'>Total Deposited: <strong>{{ totals['total_deposits'] }} RWF</strong></p>
        <p class='amount'>Total Withdrawn: <strong>{{ totals['total_withdrawals'] }} RWF</strong></p>
        <p class='amount'>Total Spent on Bundles & Fees: <strong>{{ totals['total_spent'] }} RWF</strong></p>
    </div>
</body>
</html>
"""

@app.route('/generate_template')
def generate_template():
    with open('templates/index.html', 'w') as f:
        f.write(html_template)
    return "Template successfully created!"

if __name__ == '__main__':
    app.run(debug=True)
