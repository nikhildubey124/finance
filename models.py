from extensions import db
import uuid
import hashlib
from datetime import datetime
from encryption_utils import encrypt_field, decrypt_field

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Encrypted fields - stored as longer strings to accommodate encrypted data
    _full_name = db.Column("full_name", db.String(500), nullable=False)
    _mobile_number = db.Column("mobile_number", db.String(500), nullable=False)
    _email = db.Column("email", db.String(500), nullable=False)  # Encrypted email value
    _username = db.Column("username", db.String(500), nullable=False)  # Encrypted username value

    # Hashes for lookups (since encrypted fields can't be queried directly)
    email_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    username_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(255), nullable=False)

    # Password reset fields
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

    transactions = db.relationship('Transaction', backref='user', lazy=True)

    # Properties for transparent encryption/decryption
    @property
    def full_name(self):
        """Decrypt full_name when accessed"""
        return decrypt_field(self._full_name)

    @full_name.setter
    def full_name(self, value):
        """Encrypt full_name when set"""
        self._full_name = encrypt_field(value)

    @property
    def mobile_number(self):
        """Decrypt mobile_number when accessed"""
        return decrypt_field(self._mobile_number)

    @mobile_number.setter
    def mobile_number(self, value):
        """Encrypt mobile_number when set"""
        self._mobile_number = encrypt_field(value)

    @property
    def email(self):
        """Decrypt email when accessed"""
        return decrypt_field(self._email)

    @email.setter
    def email(self, value):
        """Encrypt email when set and create hash for lookups"""
        self._email = encrypt_field(value)
        # Store SHA-256 hash of email for database lookups
        self.email_hash = hashlib.sha256(value.lower().encode()).hexdigest()

    @property
    def username(self):
        """Decrypt username when accessed"""
        return decrypt_field(self._username)

    @username.setter
    def username(self, value):
        """Encrypt username when set and create hash for lookups"""
        self._username = encrypt_field(value)
        # Store SHA-256 hash of username for database lookups
        self.username_hash = hashlib.sha256(value.lower().encode()).hexdigest()

    @staticmethod
    def hash_email(email: str) -> str:
        """Generate SHA-256 hash of email for lookup purposes"""
        return hashlib.sha256(email.lower().encode()).hexdigest()

    @staticmethod
    def hash_username(username: str) -> str:
        """Generate SHA-256 hash of username for lookup purposes"""
        return hashlib.sha256(username.lower().encode()).hexdigest()

    @staticmethod
    def find_by_email(email: str):
        """Find user by email using the hash"""
        email_hash = User.hash_email(email)
        return User.query.filter_by(email_hash=email_hash).first()

    @staticmethod
    def find_by_username(username: str):
        """Find user by username using the hash"""
        username_hash = User.hash_username(username)
        return User.query.filter_by(username_hash=username_hash).first()

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    category_type = db.Column(db.String(10), nullable=False)  # CREDIT / DEBIT

    # User ownership - NULL means system/default category
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=True)

    # Visual customization
    icon = db.Column(db.String(50), nullable=True)  # Emoji or icon class
    color = db.Column(db.String(7), nullable=True)  # Hex color code (e.g., #3498db)

    # Subcategory support
    parent_category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=True)

    # Relationships
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[category_id]), lazy=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_system_category(self):
        """Check if this is a system/default category"""
        return self.user_id is None

    def is_user_category(self):
        """Check if this is a user-created category"""
        return self.user_id is not None


class Transaction(db.Model):
    __tablename__ = "transactions"
    transaction_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"))
    transaction_type = db.Column(db.String(10))
    amount = db.Column(db.Numeric(12, 2))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"))
    transaction_date = db.Column(db.Date)
    description = db.Column(db.Text, nullable=True)  # Optional notes/description
    category = db.relationship('Category', backref='transactions')


class Budget(db.Model):
    __tablename__ = "budgets"
    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    monthly_limit = db.Column(db.Numeric(12, 2), nullable=False)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='budgets')
    category = db.relationship('Category', backref='budgets')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_id', 'month', 'year', name='unique_budget'),
    )