from flask import Blueprint, render_template, session, redirect, request
from extensions import db
from models import Transaction, Category, Budget
from sqlalchemy import func, case
from datetime import date, timedelta, datetime

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    active_user = session.get("username", "Guest")

    # =========================
    # Date Range Handling
    # =========================
    today = date.today()

    # Handle presets
    preset = request.args.get("preset")
    from_date_str = request.args.get("from_date")
    to_date_str = request.args.get("to_date")

    if preset == "last7days":
        filter_start = today - timedelta(days=7)
        filter_end = today
    elif preset == "last30days":
        filter_start = today - timedelta(days=30)
        filter_end = today
    elif preset == "thismonth":
        filter_start = today.replace(day=1)
        filter_end = today
    elif preset == "lastmonth":
        first_day_current = today.replace(day=1)
        filter_end = first_day_current - timedelta(days=1)
        filter_start = filter_end.replace(day=1)
    elif preset == "thisyear":
        filter_start = date(today.year, 1, 1)
        filter_end = today
    elif from_date_str or to_date_str:
        filter_start = datetime.strptime(from_date_str, "%Y-%m-%d").date() if from_date_str else date(2000, 1, 1)
        filter_end = datetime.strptime(to_date_str, "%Y-%m-%d").date() if to_date_str else today
    else:
        # Default: current month
        filter_start = today.replace(day=1)
        filter_end = today
        from_date_str = None
        to_date_str = None

    # For template display
    from_date_display = filter_start.strftime("%Y-%m-%d") if (from_date_str or preset) else None
    to_date_display = filter_end.strftime("%Y-%m-%d") if (to_date_str or preset) else None

    # =========================
    # Date calculations for comparisons
    # =========================
    first_day_current_month = today.replace(day=1)

    first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)
    last_day_last_month = first_day_current_month - timedelta(days=1)

    # Last year same month
    try:
        first_day_last_year_month = date(today.year - 1, today.month, 1)
        if today.month == 12:
            last_day_last_year_month = date(today.year - 1, 12, 31)
        else:
            last_day_last_year_month = date(today.year - 1, today.month + 1, 1) - timedelta(days=1)
    except ValueError:
        first_day_last_year_month = None
        last_day_last_year_month = None

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
    # Filtered Period Expense (replaces "Current Month")
    # =========================
    current_month_expense = (
        db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "DEBIT",
            Transaction.transaction_date >= filter_start,
            Transaction.transaction_date <= filter_end
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
    # Category-wise Expense (filtered)
    # =========================
    category_data = (
        db.session.query(
            Category.category_name,
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .join(Transaction, Transaction.category_id == Category.category_id)
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "DEBIT",
            Transaction.transaction_date >= filter_start,
            Transaction.transaction_date <= filter_end
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
    # Budget Alerts (Optimized - single query with joins)
    # =========================
    budget_alerts = []

    # Get all budgets with spending in one query using subquery
    budget_spending = (
        db.session.query(
            Budget.category_id,
            Budget.monthly_limit,
            Category.category_name,
            func.coalesce(func.sum(Transaction.amount), 0).label('actual_spent')
        )
        .join(Category, Budget.category_id == Category.category_id)
        .outerjoin(Transaction, (Transaction.category_id == Budget.category_id) &
                   (Transaction.user_id == user_id) &
                   (Transaction.transaction_type == "DEBIT") &
                   (Transaction.transaction_date >= first_day_current_month) &
                   (Transaction.transaction_date <= today))
        .filter(Budget.user_id == user_id,
                Budget.month == today.month,
                Budget.year == today.year)
        .group_by(Budget.category_id, Budget.monthly_limit, Category.category_name)
        .all()
    )

    for category_id, monthly_limit, category_name, actual_spent in budget_spending:
        percentage = (float(actual_spent) / float(monthly_limit) * 100) if monthly_limit > 0 else 0

        if percentage >= 80:
            budget_alerts.append({
                'category_name': category_name,
                'percentage': round(percentage, 1),
                'spent': float(actual_spent),
                'limit': float(monthly_limit),
                'status': 'danger' if percentage > 100 else 'warning'
            })

    # =========================
    # Budget vs Actual Comparison (Optimized - reuse previous query)
    # =========================
    budget_comparison = []
    total_budgeted = 0
    total_actual = 0

    # Reuse budget_spending data from previous query (already optimized)
    for category_id, monthly_limit, category_name, actual_spent in budget_spending:
        total_budgeted += float(monthly_limit)
        total_actual += float(actual_spent)

        budget_comparison.append({
            'category': category_name,
            'budget': float(monthly_limit),
            'actual': float(actual_spent),
            'variance': float(monthly_limit) - float(actual_spent)
        })

    # =========================
    # Last Year Comparison
    # =========================
    last_year_expense = 0
    if first_day_last_year_month and last_day_last_year_month:
        last_year_expense = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= first_day_last_year_month,
                Transaction.transaction_date <= last_day_last_year_month
            )
            .scalar()
        ) or 0

    # =========================
    # Daily Spending Trend (Filtered Period)
    # =========================
    daily_spending = (
        db.session.query(
            Transaction.transaction_date,
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == "DEBIT",
            Transaction.transaction_date >= filter_start,
            Transaction.transaction_date <= filter_end
        )
        .group_by(Transaction.transaction_date)
        .order_by(Transaction.transaction_date)
        .all()
    )

    daily_labels = [str(row[0]) for row in daily_spending]
    daily_values = [float(row[1]) for row in daily_spending]

    # =========================
    # Weekly Spending (Last 8 weeks)
    # =========================
    eight_weeks_ago = today - timedelta(weeks=8)
    weekly_data = []

    for i in range(8):
        week_start = eight_weeks_ago + timedelta(weeks=i)
        week_end = week_start + timedelta(days=6)

        week_spending = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= week_start,
                Transaction.transaction_date <= week_end
            )
            .scalar()
        ) or 0

        weekly_data.append({
            'week': f"Week {i+1}",
            'amount': float(week_spending)
        })

    # =========================
    # Monthly Comparison (Last 6 months)
    # =========================
    monthly_comparison = []
    for i in range(5, -1, -1):  # 6 months back to current
        month_first_day = (first_day_current_month - timedelta(days=i * 30)).replace(day=1)
        if month_first_day.month == 12:
            month_last_day = date(month_first_day.year, 12, 31)
        else:
            month_last_day = date(month_first_day.year, month_first_day.month + 1, 1) - timedelta(days=1)

        month_spending = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= month_first_day,
                Transaction.transaction_date <= month_last_day
            )
            .scalar()
        ) or 0

        monthly_comparison.append({
            'month': month_first_day.strftime('%b %Y'),
            'amount': float(month_spending)
        })

    return render_template(
        "dashboard.html",
        active_user=active_user,
        balance=round(balance, 2),
        current_month_expense=round(current_month_expense, 2),
        last_month_expense=round(last_month_expense, 2),
        last_year_expense=round(last_year_expense, 2),
        categories=categories,
        category_values=category_values,
        recent_transactions=recent_transactions,
        budget_alerts=budget_alerts,
        budget_comparison=budget_comparison,
        total_budgeted=round(total_budgeted, 2),
        total_actual=round(total_actual, 2),
        daily_labels=daily_labels,
        daily_values=daily_values,
        weekly_data=weekly_data,
        monthly_comparison=monthly_comparison,
        from_date=from_date_display,
        to_date=to_date_display
    )