"""
Migration script to encrypt existing username data
Run this AFTER running migrate_add_username_encryption.py

IMPORTANT: Backup your database before running this script!
"""
import os
import sys
from app import create_app
from extensions import db
from models import User
from encryption_utils import encrypt_field
import hashlib

def migrate_username_encryption():
    """Encrypt existing username data"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("USERNAME DATA ENCRYPTION MIGRATION")
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
        response = input("WARNING: This will encrypt username data. Have you backed up your database? (yes/no): ")
        if response.lower() != "yes":
            print("Migration cancelled. Please backup your database first.")
            return

        print()
        print("Starting username encryption migration...")
        print("-" * 60)

        migrated_count = 0
        skipped_count = 0

        for user in users:
            try:
                print(f"Processing user: {user._username if hasattr(user, '_username') else 'N/A'}")

                # Check if already encrypted (encrypted data is much longer)
                if len(user._username) > 100:
                    print(f"  [SKIP]  Skipping - already encrypted")
                    skipped_count += 1
                    continue

                # Store original value
                original_username = user._username

                # Encrypt username
                user._username = encrypt_field(original_username)

                # Create username hash for lookups
                user.username_hash = hashlib.sha256(original_username.lower().encode()).hexdigest()

                print(f"  [OK] Encrypted: {original_username} -> [ENCRYPTED]")
                print(f"  [OK] Username hash created for lookups")

                migrated_count += 1

            except Exception as e:
                print(f"  [ERROR] Error encrypting username: {str(e)}")
                db.session.rollback()
                continue

        # Commit all changes
        try:
            db.session.commit()
            print()
            print("=" * 60)
            print("MIGRATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"[OK] Migrated: {migrated_count} user(s)")
            print(f"[SKIP]  Skipped: {skipped_count} user(s)")
            print()
            print("Username data is now encrypted!")
            print()
        except Exception as e:
            db.session.rollback()
            print()
            print("[ERROR] ERROR: Failed to commit changes to database")
            print(f"Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    migrate_username_encryption()
