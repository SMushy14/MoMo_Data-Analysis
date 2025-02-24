from flask import Flask, request, render_template_string
import sqlite3
import os
from werkzeug.utils import secure_filename
from parser2 import parse_uploaded_xml

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Transaction Records</title>
</head>
<body>
    <h2>Upload XML File</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload & Parse</button>
    </form>
    <h2>Transaction Records</h2>
    <table border="1">
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

def get_transactions():
    conn = sqlite3.connect("parsed_data2.db")
    cursor = conn.cursor()
    cursor.execute("SELECT transaction_id, amount, date_time, transaction_type FROM transactions")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

@app.route('/')
def display_transactions():
    transactions = get_transactions()
    return render_template_string(TEMPLATE, transactions=transactions)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    parse_uploaded_xml(file_path)
    return "File uploaded and parsed successfully! <a href='/'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)
