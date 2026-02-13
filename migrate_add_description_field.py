"""
Database Migration: Add Description Field to Transactions
==========================================================
Adds an optional description field to the transactions table
for users to add notes and context to their transactions.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_add_description():
    print("[INFO] Adding description field to transactions table...")

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    try:
        # Add description column
        print("  - Adding 'description' column to transactions table...")
        cursor.execute("""
            ALTER TABLE transactions
            ADD COLUMN IF NOT EXISTS description TEXT;
        """)

        conn.commit()
        print("[OK] Description field added successfully!")
        print("[INFO] Users can now add notes to their transactions.")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {str(e)}")
        raise

    finally:
        cursor.close()
        conn.close()
        print("[INFO] Database connection closed.")

if __name__ == "__main__":
    migrate_add_description()
