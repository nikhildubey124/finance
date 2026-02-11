from flask import Blueprint, render_template, request, redirect, session, current_app, Response
from extensions import db
from models import Transaction, Category
from datetime import date
from io import StringIO
import csv

txn_bp = Blueprint("transactions", __name__)

@txn_bp.route("/add-transaction", methods=["GET", "POST"])
def add_transaction():
    if "user_id" not in session:
        return redirect("/")

    # Default type
    txn_type = request.args.get("type", "DEBIT")

    # Load categories based on type
    categories = Category.query.filter_by(category_type=txn_type).all()

    if request.method == "POST":
        try:
            username = session.get("username", "Unknown")
            transaction_type = request.form.get("type")
            amount = request.form.get("amount")
            category_id = request.form.get("category_id")

            current_app.logger.debug(f"Transaction form submitted by {username}: Type={transaction_type}, Amount={amount}")

            # HARD VALIDATION
            if not transaction_type or not amount or not category_id:
                current_app.logger.warning(f"Missing transaction data from user {username}")
                return "Missing form data", 400

            txn = Transaction(
                user_id=session["user_id"],
                transaction_type=transaction_type.upper().strip(),
                amount=float(amount),
                category_id=int(category_id),
                transaction_date=date.today()
            )

            db.session.add(txn)
            db.session.commit()

            current_app.logger.info(f"Transaction added - User: {username}, Type: {transaction_type}, Amount: {amount}, Category ID: {category_id}")

            return redirect("/dashboard")

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Transaction insertion error - User: {session.get('username', 'Unknown')}, Error: {str(e)}")
            return "Error inserting transaction", 500

    return render_template(
        "add_transaction.html",
        categories=categories,
        txn_type=txn_type
    )


@txn_bp.route("/export-transactions")
def export_transactions():
    """Export all user transactions to CSV file"""
    if "user_id" not in session:
        return redirect("/")

    try:
        user_id = session["user_id"]
        username = session.get("username", "user")

        # Get all transactions with category names
        transactions = (
            db.session.query(
                Transaction.transaction_date,
                Transaction.transaction_type,
                Category.category_name,
                Transaction.amount
            )
            .join(Category, Transaction.category_id == Category.category_id)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.transaction_date.desc())
            .all()
        )

        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow(['Date', 'Type', 'Category', 'Amount'])

        # Write transaction data
        for txn in transactions:
            writer.writerow([
                txn.transaction_date.strftime('%Y-%m-%d'),
                txn.transaction_type,
                txn.category_name,
                float(txn.amount)
            ])

        output.seek(0)

        current_app.logger.info(f"CSV export - User: {username}, Transactions: {len(transactions)}")

        # Return as downloadable file
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={username}_transactions.csv'
            }
        )

    except Exception as e:
        current_app.logger.error(f"CSV export error - User: {session.get('username', 'Unknown')}, Error: {str(e)}")
        return "Error exporting transactions", 500
