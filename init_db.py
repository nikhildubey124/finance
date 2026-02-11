"""
Initialize database tables for the application
"""
from app import app
from extensions import db

def init_database():
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("[OK] Database tables created successfully!")
            print("[OK] Database is ready!")
            return True
        except Exception as e:
            print(f"[ERROR] Error initializing database: {e}")
            return False

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
