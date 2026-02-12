"""
Database schema migration to add category management features
Adds user_id, icon, color, parent_category_id, and created_at columns

Run this to enable custom categories, icons/colors, and subcategories
"""
from app import create_app
from extensions import db
from sqlalchemy import text

def migrate_schema():
    """Add category management columns"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("DATABASE SCHEMA MIGRATION - CATEGORY MANAGEMENT")
        print("=" * 60)
        print()

        # Ask for confirmation
        response = input("WARNING: This will modify the categories table. Have you backed up your database? (yes/no): ")
        if response.lower() != "yes":
            print("Migration cancelled. Please backup your database first.")
            return

        print()
        print("Starting schema migration...")
        print("-" * 60)

        try:
            # Add user_id column for user-specific categories
            print("1. Adding user_id column...")
            db.session.execute(text("""
                ALTER TABLE categories
                ADD COLUMN IF NOT EXISTS user_id VARCHAR(36);
            """))
            print("   [OK] user_id column added")

            # Add foreign key constraint for user_id
            print("2. Adding user_id foreign key constraint...")
            try:
                db.session.execute(text("""
                    ALTER TABLE categories
                    ADD CONSTRAINT fk_categories_user_id
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                    ON DELETE CASCADE;
                """))
                print("   [OK] Foreign key constraint added")
            except Exception as e:
                print(f"   [WARNING] Note: {str(e)}")

            # Add icon column
            print("3. Adding icon column...")
            db.session.execute(text("""
                ALTER TABLE categories
                ADD COLUMN IF NOT EXISTS icon VARCHAR(50);
            """))
            print("   [OK] icon column added")

            # Add color column
            print("4. Adding color column...")
            db.session.execute(text("""
                ALTER TABLE categories
                ADD COLUMN IF NOT EXISTS color VARCHAR(7);
            """))
            print("   [OK] color column added")

            # Add parent_category_id column for subcategories
            print("5. Adding parent_category_id column...")
            db.session.execute(text("""
                ALTER TABLE categories
                ADD COLUMN IF NOT EXISTS parent_category_id INTEGER;
            """))
            print("   [OK] parent_category_id column added")

            # Add foreign key constraint for parent_category_id
            print("6. Adding parent_category_id foreign key constraint...")
            try:
                db.session.execute(text("""
                    ALTER TABLE categories
                    ADD CONSTRAINT fk_categories_parent_id
                    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
                    ON DELETE CASCADE;
                """))
                print("   [OK] Foreign key constraint added")
            except Exception as e:
                print(f"   [WARNING] Note: {str(e)}")

            # Add created_at column
            print("7. Adding created_at column...")
            db.session.execute(text("""
                ALTER TABLE categories
                ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """))
            print("   [OK] created_at column added")

            # Commit all changes
            db.session.commit()

            print()
            print("=" * 60)
            print("SCHEMA MIGRATION COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print()
            print("Category management features are now enabled!")
            print("- Custom user categories")
            print("- Category icons and colors")
            print("- Subcategory support")
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
