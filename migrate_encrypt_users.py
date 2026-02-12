"""
Migration script to encrypt existing user data
Run this once to encrypt all existing user personal information

IMPORTANT: Backup your database before running this script!
"""
import os
import sys
from app import create_app
from extensions import db
from models import User
from encryption_utils import encrypt_field
import hashlib

def migrate_user_encryption():
    """Encrypt existing user data"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("USER DATA ENCRYPTION MIGRATION")
        print("=" * 60)
        print()

        # Get all users
        users = db.session.query(User).all()

        if not users:
            print("No users found in database.")
            return

        print(f"Found {len(users)} user(s) to encrypt.")
        print()

        # Ask for confirmation
        response = input("⚠️  WARNING: This will modify user data. Have you backed up your database? (yes/no): ")
        if response.lower() != "yes":
            print("Migration cancelled. Please backup your database first.")
            return

        print()
        print("Starting encryption migration...")
        print("-" * 60)

        migrated_count = 0
        skipped_count = 0

        for user in users:
            try:
                print(f"Processing user: {user.username}")

                # Check if already encrypted (encrypted data is much longer)
                if len(user._full_name) > 200 or len(user._mobile_number) > 100:
                    print(f"  ⏭️  Skipping - already encrypted")
                    skipped_count += 1
                    continue

                # Store original values
                original_name = user._full_name
                original_mobile = user._mobile_number
                original_email = user._email

                # Encrypt fields
                user._full_name = encrypt_field(original_name)
                user._mobile_number = encrypt_field(original_mobile)
                user._email = encrypt_field(original_email)

                # Create email hash for lookups
                user.email_hash = hashlib.sha256(original_email.lower().encode()).hexdigest()

                print(f"  ✅ Encrypted: {original_name} -> [ENCRYPTED]")
                print(f"  ✅ Email hash created for lookups")

                migrated_count += 1

            except Exception as e:
                print(f"  ❌ Error encrypting user {user.username}: {str(e)}")
                db.session.rollback()
                continue

        # Commit all changes
        try:
            db.session.commit()
            print()
            print("=" * 60)
            print("MIGRATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"✅ Migrated: {migrated_count} user(s)")
            print(f"⏭️  Skipped: {skipped_count} user(s)")
            print()
            print("User data is now encrypted!")
            print()
        except Exception as e:
            db.session.rollback()
            print()
            print("❌ ERROR: Failed to commit changes to database")
            print(f"Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    migrate_user_encryption()
