import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask secret key (used for sessions)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")

    # Aiven PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration (Flask-Mail)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))
