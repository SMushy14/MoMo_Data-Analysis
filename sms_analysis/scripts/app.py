from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM transactions"
    filters = []
    
    transaction_type = request.args.get('type')
    if transaction_type:
        query += " WHERE type = ?"
        filters.append(transaction_type)
    
    cursor.execute(query, filters)
    transactions = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in transactions])

if __name__ == '__main__':
    app.run(debug=True)
