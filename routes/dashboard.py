from flask import Blueprint, render_template, session, redirect
from extensions import db
from models import Transaction, Category, Budget
from sqlalchemy import func, case
from datetime import date, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    active_user = session.get("username", "Guest")

    # =========================
    # Date calculations
    # =========================
    today = date.today()
    first_day_current_month = today.replace(day=1)

    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)
    last_day_last_month = first_day_current_month - timedelta(days=1)

    # =========================
    # Current Balance
    # =========================
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

    # =========================
    # Current Month Expense
    # =========================
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

    # =========================
    # Last Month Expense
    # =========================
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

    # =========================
    # Category-wise Expense
    # =========================
    category_data = (
        db.session.query(
            Category.category_name,
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .join(Transaction, Transaction.category_id == Category.category_id)
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "DEBIT"
        )
        .group_by(Category.category_name)
        .all()
    )

    # Safe defaults for new users
    categories = [row[0] for row in category_data] if category_data else []
    category_values = [float(row[1]) for row in category_data] if category_data else []


    recent_transactions = (
        db.session.query(
            Transaction.transaction_type,
            Transaction.amount,
            Category.category_name
        )
        .join(Category, Transaction.category_id == Category.category_id)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.transaction_date.desc())
        .limit(5)
        .all()
    )

    # =========================
    # Budget Alerts
    # =========================
    budget_alerts = []
    budgets = Budget.query.filter_by(
        user_id=user_id,
        month=today.month,
        year=today.year
    ).all()

    for budget in budgets:
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

        if percentage >= 80:
            category = Category.query.get(budget.category_id)
            budget_alerts.append({
                'category_name': category.category_name,
                'percentage': round(percentage, 1),
                'spent': float(actual_spent),
                'limit': float(budget.monthly_limit),
                'status': 'danger' if percentage > 100 else 'warning'
            })

    return render_template(
        "dashboard.html",
        active_user=active_user,
        balance=round(balance, 2),
        current_month_expense=round(current_month_expense, 2),
        last_month_expense=round(last_month_expense, 2),
        categories=categories,
        category_values=category_values,
        recent_transactions=recent_transactions,
        budget_alerts=budget_alerts
    )