from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('transactions.db')
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM transactions"
    filters = []
    
    transaction_type = request.args.get('type')
    if transaction_type:
        query += " WHERE category = ?"
        filters.append(transaction_type)
    
    cur.execute(query, filters)
    transactions = cur.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in transactions])

@app.route('/transaction/<int:id>', methods=['GET'])
def get_transaction(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions WHERE id = ?", (id,))
    transaction = cur.fetchone()
    conn.close()
    
    if transaction:
        return jsonify(dict(transaction))
    else:
        return jsonify({'error': 'Transaction not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
