from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(100))
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
