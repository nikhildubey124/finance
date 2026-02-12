"""
Database schema migration to add encryption support
Adds email_hash column and increases column sizes for encrypted data

Run this BEFORE running migrate_encrypt_users.py
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def migrate_schema():
    """Add encryption-related columns and modify existing ones"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("DATABASE SCHEMA MIGRATION - ADD ENCRYPTION SUPPORT")
        print("=" * 60)
        print()

        # Ask for confirmation
        response = input("WARNING: This will modify the database schema. Have you backed up your database? (yes/no): ")
        if response.lower() != "yes":
            print("Migration cancelled. Please backup your database first.")
            return

        print()
        print("Starting schema migration...")
        print("-" * 60)

        try:
            # Add email_hash column
            print("1. Adding email_hash column...")
            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS email_hash VARCHAR(64);
            """))
            print("   [OK] email_hash column added")

            # Create index on email_hash for faster lookups
            print("2. Creating index on email_hash...")
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_email_hash
                ON users(email_hash);
            """))
            print("   [OK] Index created")

            # Modify column sizes to accommodate encrypted data
            print("3. Increasing column sizes for encrypted data...")

            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN full_name TYPE VARCHAR(500);
            """))
            print("   [OK] full_name column expanded")

            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN mobile_number TYPE VARCHAR(500);
            """))
            print("   [OK] mobile_number column expanded")

            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN email TYPE VARCHAR(500);
            """))
            print("   [OK] email column expanded")

            # Drop unique constraint on email (will use email_hash instead)
            print("4. Updating email constraints...")
            try:
                # PostgreSQL syntax for dropping constraint
                db.session.execute(text("""
                    ALTER TABLE users
                    DROP CONSTRAINT IF EXISTS users_email_key;
                """))
                print("   [OK] Old email unique constraint removed")
            except Exception as e:
                print(f"   [WARNING]  Note: {str(e)}")

            # Add unique constraint on email_hash
            db.session.execute(text("""
                ALTER TABLE users
                ADD CONSTRAINT users_email_hash_key UNIQUE (email_hash);
            """))
            print("   [OK] email_hash unique constraint added")

            # Commit all changes
            db.session.commit()

            print()
            print("=" * 60)
            print("SCHEMA MIGRATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print()
            print("Next step: Run migrate_encrypt_users.py to encrypt existing data")
            print()

        except Exception as e:
            db.session.rollback()
            print()
            print("[ERROR] ERROR: Schema migration failed")
            print(f"Error: {str(e)}")
            print()
            print("Please review the error and try again.")
            return


if __name__ == "__main__":
    migrate_schema()
