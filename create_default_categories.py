"""
Create Default System Categories
=================================
Creates a comprehensive set of default categories for both
Credit (Income) and Debit (Expense) transactions.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Default categories configuration
DEFAULT_CATEGORIES = {
    'CREDIT': [
        ('Salary', '💰', '#27ae60'),
        ('Bonus', '🎁', '#2ecc71'),
        ('Freelance Income', '💼', '#3498db'),
        ('Business Income', '🏢', '#1abc9c'),
        ('Investment Returns', '📈', '#16a085'),
        ('Rental Income', '🏠', '#27ae60'),
        ('Gift Received', '🎉', '#9b59b6'),
        ('Refund', '↩️', '#95a5a6'),
        ('Interest Earned', '💹', '#27ae60'),
        ('Other Income', '💵', '#7f8c8d'),
    ],
    'DEBIT': [
        ('Food & Dining', '🍔', '#e74c3c'),
        ('Groceries', '🛒', '#e67e22'),
        ('Transportation', '🚗', '#3498db'),
        ('Housing/Rent', '🏠', '#9b59b6'),
        ('Utilities', '💡', '#f39c12'),
        ('Healthcare', '⚕️', '#e74c3c'),
        ('Shopping', '🛍️', '#e91e63'),
        ('Entertainment', '🎬', '#9c27b0'),
        ('Education', '📚', '#2196f3'),
        ('Travel', '✈️', '#00bcd4'),
        ('Insurance', '🛡️', '#607d8b'),
        ('Loan Payment', '🏦', '#f44336'),
        ('Investment', '📊', '#4caf50'),
        ('Gifts & Donations', '🎁', '#ff9800'),
        ('Personal Care', '💆', '#e91e63'),
        ('Fitness & Sports', '⚽', '#4caf50'),
        ('Bills & Fees', '📄', '#ff5722'),
        ('Subscriptions', '📱', '#673ab7'),
        ('Pet Care', '🐾', '#795548'),
        ('Other Expense', '💸', '#9e9e9e'),
    ]
}

def create_default_categories():
    print("[INFO] Creating default system categories...")
    print("=" * 60)

    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    try:
        total_created = 0
        total_skipped = 0

        for category_type, categories in DEFAULT_CATEGORIES.items():
            print(f"\n{category_type} Categories:")
            print("-" * 40)

            for category_name, icon, color in categories:
                # Check if category already exists
                cursor.execute("""
                    SELECT category_id FROM categories
                    WHERE category_name = %s
                    AND category_type = %s
                    AND user_id IS NULL
                """, (category_name, category_type))

                if cursor.fetchone():
                    print(f"  [SKIP] {category_name} - Already exists")
                    total_skipped += 1
                else:
                    # Insert new category
                    cursor.execute("""
                        INSERT INTO categories (category_name, category_type, user_id, icon, color)
                        VALUES (%s, %s, NULL, %s, %s)
                    """, (category_name, category_type, icon, color))

                    print(f"  [OK] {category_name}")
                    total_created += 1

        conn.commit()

        print("\n" + "=" * 60)
        print(f"[OK] Default categories setup complete!")
        print(f"  - Created: {total_created} categories")
        print(f"  - Skipped: {total_skipped} categories (already exist)")
        print(f"  - Total: {total_created + total_skipped} categories")

        # Show summary by type
        cursor.execute("""
            SELECT category_type, COUNT(*)
            FROM categories
            WHERE user_id IS NULL
            GROUP BY category_type
            ORDER BY category_type
        """)

        print("\nSystem Categories Summary:")
        for cat_type, count in cursor.fetchall():
            print(f"  {cat_type}: {count} categories")

    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Failed to create categories: {str(e)}")
        raise

    finally:
        cursor.close()
        conn.close()
        print("\n[INFO] Database connection closed.")

if __name__ == "__main__":
    create_default_categories()
