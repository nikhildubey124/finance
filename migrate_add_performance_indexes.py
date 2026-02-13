"""
Database Migration: Add Performance Indexes
===========================================
This script adds database indexes to improve query performance.
Indexes are added on frequently queried columns to speed up searches and joins.

Run this script once to optimize database performance.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_add_indexes():
    print("[INFO] Starting database index migration for performance optimization...")

    # Connect to PostgreSQL
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    try:
        print("[INFO] Adding indexes to improve query performance...")

        # ===== TRANSACTIONS TABLE INDEXES =====
        # Index on user_id for fast user-specific queries
        print("  - Creating index on transactions(user_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_id
            ON transactions(user_id);
        """)

        # Index on transaction_date for date range queries
        print("  - Creating index on transactions(transaction_date)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_date
            ON transactions(transaction_date);
        """)

        # Composite index for user + date queries (most common pattern)
        print("  - Creating composite index on transactions(user_id, transaction_date)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_date
            ON transactions(user_id, transaction_date DESC);
        """)

        # Index on category_id for category-based filtering
        print("  - Creating index on transactions(category_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_category
            ON transactions(category_id);
        """)

        # Index on transaction_type for type filtering
        print("  - Creating index on transactions(transaction_type)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_type
            ON transactions(transaction_type);
        """)

        # Composite index for user + type queries
        print("  - Creating composite index on transactions(user_id, transaction_type)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_type
            ON transactions(user_id, transaction_type);
        """)

        # Composite index for user + category queries
        print("  - Creating composite index on transactions(user_id, category_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_transactions_user_category
            ON transactions(user_id, category_id);
        """)

        # ===== BUDGETS TABLE INDEXES =====
        # Index on user_id for user-specific budget queries
        print("  - Creating index on budgets(user_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_budgets_user_id
            ON budgets(user_id);
        """)

        # Composite index for month/year queries
        print("  - Creating composite index on budgets(user_id, month, year)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_budgets_user_month_year
            ON budgets(user_id, month, year);
        """)

        # Index on category_id for budget-category joins
        print("  - Creating index on budgets(category_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_budgets_category
            ON budgets(category_id);
        """)

        # ===== CATEGORIES TABLE INDEXES =====
        # Index on user_id for user-specific categories
        print("  - Creating index on categories(user_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_categories_user_id
            ON categories(user_id);
        """)

        # Index on category_type for type filtering
        print("  - Creating index on categories(category_type)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_categories_type
            ON categories(category_type);
        """)

        # Composite index for user + type queries
        print("  - Creating composite index on categories(user_id, category_type)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_categories_user_type
            ON categories(user_id, category_type);
        """)

        # Index on parent_category_id for subcategory queries
        print("  - Creating index on categories(parent_category_id)...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_categories_parent
            ON categories(parent_category_id);
        """)

        # ===== USERS TABLE INDEXES =====
        # Indexes on hash columns already exist (created with unique constraint)
        # But let's verify they're optimized
        print("  - Verifying indexes on users table...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email_hash
            ON users(email_hash);
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_username_hash
            ON users(username_hash);
        """)

        # Commit all changes
        conn.commit()
        print("[OK] All indexes created successfully!")
        print("[INFO] Database query performance has been optimized.")

        # Show statistics
        print("\n[INFO] Index Statistics:")
        cursor.execute("""
            SELECT schemaname, tablename, indexname
            FROM pg_indexes
            WHERE schemaname = 'public'
            ORDER BY tablename, indexname;
        """)

        indexes = cursor.fetchall()
        current_table = None
        for schema, table, index in indexes:
            if table != current_table:
                print(f"\n  {table}:")
                current_table = table
            print(f"    - {index}")

        print(f"\n[OK] Total indexes: {len(indexes)}")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {str(e)}")
        raise

    finally:
        cursor.close()
        conn.close()
        print("[INFO] Database connection closed.")

if __name__ == "__main__":
    migrate_add_indexes()
