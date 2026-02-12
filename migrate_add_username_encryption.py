"""
Database schema migration to add username encryption support
Adds username_hash column and increases username column size

Run this BEFORE updating existing username data
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def migrate_schema():
    """Add username encryption columns and modify existing ones"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("DATABASE SCHEMA MIGRATION - USERNAME ENCRYPTION SUPPORT")
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
            # Add username_hash column
            print("1. Adding username_hash column...")
            db.session.execute(text("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS username_hash VARCHAR(64);
            """))
            print("   [OK] username_hash column added")

            # Create index on username_hash for faster lookups
            print("2. Creating index on username_hash...")
            db.session.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_users_username_hash
                ON users(username_hash);
            """))
            print("   [OK] Index created")

            # Modify username column size to accommodate encrypted data
            print("3. Increasing username column size for encrypted data...")
            db.session.execute(text("""
                ALTER TABLE users
                ALTER COLUMN username TYPE VARCHAR(500);
            """))
            print("   [OK] username column expanded")

            # Drop unique constraint on username (will use username_hash instead)
            print("4. Updating username constraints...")
            try:
                # PostgreSQL syntax for dropping constraint
                db.session.execute(text("""
                    ALTER TABLE users
                    DROP CONSTRAINT IF EXISTS users_username_key;
                """))
                print("   [OK] Old username unique constraint removed")
            except Exception as e:
                print(f"   [WARNING]  Note: {str(e)}")

            # Add unique constraint on username_hash
            db.session.execute(text("""
                ALTER TABLE users
                ADD CONSTRAINT users_username_hash_key UNIQUE (username_hash);
            """))
            print("   [OK] username_hash unique constraint added")

            # Commit all changes
            db.session.commit()

            print()
            print("=" * 60)
            print("SCHEMA MIGRATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print()
            print("Next step: Run migrate_encrypt_usernames.py to encrypt existing username data")
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
