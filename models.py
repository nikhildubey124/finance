from extensions import db
import uuid
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Password reset fields
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_type = db.Column(db.String(10), nullable=False)  # CREDIT / DEBIT


class Transaction(db.Model):
    __tablename__ = "transactions"
    transaction_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"))
    transaction_type = db.Column(db.String(10))
    amount = db.Column(db.Numeric(12, 2))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    transaction_date = db.Column(db.Date)
    category = db.relationship('Category', backref='transactions')