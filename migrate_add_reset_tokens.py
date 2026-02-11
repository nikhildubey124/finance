"""
Database Migration: Add password reset token fields to users table

This script adds the following columns to the users table:
- reset_token: VARCHAR(255) - Stores hashed password reset tokens
- reset_token_expiry: TIMESTAMP - Stores when the token expires

Run this script once to update your database schema.
"""

from app import app
from extensions import db

def migrate():
    with app.app_context():
        # Execute SQL to add new columns
        try:
            with db.engine.connect() as connection:
                # Add reset_token column
                connection.execute(db.text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255)"
                ))
                connection.commit()
                print("[OK] Added reset_token column")

                # Add reset_token_expiry column
                connection.execute(db.text(
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expiry TIMESTAMP"
                ))
                connection.commit()
                print("[OK] Added reset_token_expiry column")

                print("\n[SUCCESS] Migration completed successfully!")
                print("Your database is now ready for secure password reset functionality.")

        except Exception as e:
            print(f"[ERROR] Migration failed: {e}")
            print("\nIf columns already exist, this is normal. Check your database schema.")

if __name__ == "__main__":
    print("Starting database migration...")
    print("Adding password reset token fields to users table...\n")
    migrate()
