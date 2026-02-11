from flask import Blueprint, render_template, request, redirect, session, current_app, Response
from extensions import db
from models import Transaction, Category, Budget
from datetime import date, timedelta
from sqlalchemy import func, case
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
    """Export comprehensive financial report with transactions, budgets, and analysis"""
    if "user_id" not in session:
        return redirect("/")

    try:
        user_id = session["user_id"]
        username = session.get("username", "user")

        # Date calculations
        today = date.today()
        first_day_current_month = today.replace(day=1)
        first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)
        last_day_last_month = first_day_current_month - timedelta(days=1)

        # Create CSV in memory
        output = StringIO()
        writer = csv.writer(output)

        # ==================== SECTION 1: SUMMARY ====================
        writer.writerow(['FINANCIAL SUMMARY REPORT'])
        writer.writerow(['Generated:', today.strftime('%Y-%m-%d %H:%M')])
        writer.writerow(['User:', username])
        writer.writerow([])

        # Calculate overall balance
        balance = (
            db.session.query(
                func.coalesce(
                    func.sum(
                        case(
                            (Transaction.transaction_type == "CREDIT", Transaction.amount),
                            else_=-Transaction.amount
                        )
                    ),
                    0
                )
            )
            .filter(Transaction.user_id == user_id)
            .scalar()
        ) or 0

        # Current month expense
        current_month_expense = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= first_day_current_month,
                Transaction.transaction_date <= today
            )
            .scalar()
        ) or 0

        # Last month expense
        last_month_expense = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= first_day_last_month,
                Transaction.transaction_date <= last_day_last_month
            )
            .scalar()
        ) or 0

        # Current month income
        current_month_income = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "CREDIT",
                Transaction.transaction_date >= first_day_current_month,
                Transaction.transaction_date <= today
            )
            .scalar()
        ) or 0

        writer.writerow(['OVERALL FINANCIAL HEALTH'])
        writer.writerow(['Current Balance', float(balance)])
        writer.writerow(['Current Month Income', float(current_month_income)])
        writer.writerow(['Current Month Expense', float(current_month_expense)])
        writer.writerow(['Last Month Expense', float(last_month_expense)])

        # Month over month comparison
        if last_month_expense > 0:
            change_pct = ((float(current_month_expense) - float(last_month_expense)) / float(last_month_expense)) * 100
            change_direction = "INCREASE" if change_pct > 0 else "DECREASE"
            writer.writerow(['Month-over-Month Change', f'{abs(change_pct):.1f}% {change_direction}'])
        else:
            writer.writerow(['Month-over-Month Change', 'N/A (No previous data)'])

        writer.writerow([])

        # ==================== SECTION 2: BUDGET ANALYSIS ====================
        writer.writerow(['BUDGET vs ACTUAL COMPARISON'])
        writer.writerow(['Category', 'Budget Limit', 'Actual Spent', 'Remaining', 'Usage %', 'Status'])

        budgets = Budget.query.filter_by(
            user_id=user_id,
            month=today.month,
            year=today.year
        ).all()

        total_budget = 0
        total_spent_against_budget = 0
        over_budget_count = 0

        for budget in budgets:
            category = Category.query.get(budget.category_id)

            actual_spent = (
                db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
                .filter(
                    Transaction.user_id == user_id,
                    Transaction.category_id == budget.category_id,
                    Transaction.transaction_type == "DEBIT",
                    Transaction.transaction_date >= first_day_current_month,
                    Transaction.transaction_date <= today
                )
                .scalar()
            ) or 0

            percentage = (float(actual_spent) / float(budget.monthly_limit) * 100) if budget.monthly_limit > 0 else 0
            remaining = float(budget.monthly_limit) - float(actual_spent)

            if percentage > 100:
                status = "OVER BUDGET"
                over_budget_count += 1
            elif percentage >= 80:
                status = "WARNING"
            else:
                status = "ON TRACK"

            total_budget += float(budget.monthly_limit)
            total_spent_against_budget += float(actual_spent)

            writer.writerow([
                category.category_name,
                float(budget.monthly_limit),
                float(actual_spent),
                remaining,
                f'{percentage:.1f}%',
                status
            ])

        if budgets:
            writer.writerow([])
            writer.writerow(['BUDGET SUMMARY'])
            writer.writerow(['Total Budget Allocated', total_budget])
            writer.writerow(['Total Spent Against Budget', total_spent_against_budget])
            writer.writerow(['Categories Over Budget', over_budget_count])
            overall_budget_usage = (total_spent_against_budget / total_budget * 100) if total_budget > 0 else 0
            writer.writerow(['Overall Budget Usage', f'{overall_budget_usage:.1f}%'])
        else:
            writer.writerow(['No budgets set for current month'])

        writer.writerow([])

        # ==================== SECTION 3: CATEGORY BREAKDOWN ====================
        writer.writerow(['SPENDING BY CATEGORY (Current Month)'])
        writer.writerow(['Category', 'Amount', '% of Total Spending'])

        category_spending = (
            db.session.query(
                Category.category_name,
                func.coalesce(func.sum(Transaction.amount), 0)
            )
            .join(Transaction, Transaction.category_id == Category.category_id)
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= first_day_current_month,
                Transaction.transaction_date <= today
            )
            .group_by(Category.category_name)
            .order_by(func.sum(Transaction.amount).desc())
            .all()
        )

        for cat_name, amount in category_spending:
            pct = (float(amount) / float(current_month_expense) * 100) if current_month_expense > 0 else 0
            writer.writerow([cat_name, float(amount), f'{pct:.1f}%'])

        writer.writerow([])

        # ==================== SECTION 4: ANALYSIS & INSIGHTS ====================
        writer.writerow(['FINANCIAL ANALYSIS & INSIGHTS'])

        # Insight 1: Spending trend
        if last_month_expense > 0:
            diff = float(abs(current_month_expense - last_month_expense))
            if current_month_expense > last_month_expense:
                writer.writerow(['Spending Trend', f'Your spending increased by {diff:.2f} compared to last month'])
            else:
                writer.writerow(['Spending Trend', f'Good! You saved {diff:.2f} compared to last month'])

        # Insight 2: Budget health
        if budgets:
            if over_budget_count > 0:
                writer.writerow(['Budget Health', f'ATTENTION: {over_budget_count} categor{"y is" if over_budget_count == 1 else "ies are"} over budget'])
            else:
                writer.writerow(['Budget Health', 'Excellent! All categories are within budget'])

        # Insight 3: Savings rate
        if current_month_income > 0:
            savings = float(current_month_income) - float(current_month_expense)
            savings_rate = (savings / float(current_month_income)) * 100
            writer.writerow(['Savings Rate', f'{savings_rate:.1f}% ({savings:.2f} saved this month)'])

        # Insight 4: Top spending category
        if category_spending:
            top_category, top_amount = category_spending[0]
            writer.writerow(['Top Spending Category', f'{top_category} ({float(top_amount):.2f})'])

        writer.writerow([])
        writer.writerow([])

        # ==================== SECTION 5: TRANSACTION DETAILS ====================
        writer.writerow(['DETAILED TRANSACTION HISTORY'])
        writer.writerow(['Date', 'Type', 'Category', 'Amount'])

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

        for txn in transactions:
            writer.writerow([
                txn.transaction_date.strftime('%Y-%m-%d'),
                txn.transaction_type,
                txn.category_name,
                float(txn.amount)
            ])

        output.seek(0)

        current_app.logger.info(f"Comprehensive CSV export - User: {username}, Transactions: {len(transactions)}, Budgets: {len(budgets)}")

        # Return as downloadable file
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={username}_financial_report_{today.strftime("%Y%m%d")}.csv'
            }
        )

    except Exception as e:
        current_app.logger.error(f"CSV export error - User: {session.get('username', 'Unknown')}, Error: {str(e)}")
        return "Error exporting transactions", 500
