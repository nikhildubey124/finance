import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask secret key (used for sessions)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-this")

    # Aiven PostgreSQL connection
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ===== DATABASE CONNECTION POOLING =====
    # Optimize database connections for better performance and stability
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,           # Number of connections to maintain in pool
        'pool_recycle': 3600,      # Recycle connections after 1 hour (prevents stale connections)
        'pool_pre_ping': True,     # Verify connections before using them (prevents dead connections)
        'max_overflow': 20,        # Additional connections if pool is exhausted
        'pool_timeout': 30,        # Timeout when getting connection from pool
        'connect_args': {
            'connect_timeout': 10,  # PostgreSQL connection timeout
            'options': '-c statement_timeout=30000'  # Query timeout 30 seconds
        }
    }

    # ===== FLASK-CACHING CONFIGURATION =====
    # Cache frequently accessed data for better performance
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")  # Use Redis in production
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default cache timeout
    CACHE_KEY_PREFIX = "financetracker_"

    # Redis configuration (if using Redis cache)
    CACHE_REDIS_URL = os.getenv("REDIS_URL", None)

    # ===== SESSION CONFIGURATION =====
    # Improve session security and performance
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
    SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours session timeout

    # ===== REQUEST CONFIGURATION =====
    # Stability improvements
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload size

    # Email Configuration (Flask-Mail)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))
