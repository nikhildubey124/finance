"""
Migration script to add budgets table
Run this once to create the budgets table in your database
"""
from app import app
from extensions import db
from config import Config

def migrate():
    with app.app_context():
        # SQL to create budgets table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS budgets (
            budget_id SERIAL PRIMARY KEY,
            user_id VARCHAR(36) NOT NULL,
            category_id INTEGER NOT NULL,
            monthly_limit NUMERIC(12, 2) NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE,
            CONSTRAINT unique_budget UNIQUE (user_id, category_id, month, year)
        );
        """

        try:
            db.session.execute(db.text(create_table_sql))
            db.session.commit()
            print("SUCCESS: Budgets table created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"ERROR: Error creating budgets table: {e}")

if __name__ == "__main__":
    migrate()
