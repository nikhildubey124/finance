from flask import Blueprint, render_template, request, redirect, session, current_app
from extensions import db
from models import Budget, Category, Transaction
from sqlalchemy import func
from datetime import date

budget_bp = Blueprint("budgets", __name__)


@budget_bp.route("/budgets")
def view_budgets():
    """View all budgets for current month"""
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    current_month = date.today().month
    current_year = date.today().year

    # Get all budgets for current month
    budgets = (
        db.session.query(
            Budget,
            Category.category_name,
            Category.category_type
        )
        .join(Category, Budget.category_id == Category.category_id)
        .filter(
            Budget.user_id == user_id,
            Budget.month == current_month,
            Budget.year == current_year
        )
        .all()
    )

    # Calculate actual spending for each budget
    budget_data = []
    for budget, category_name, category_type in budgets:
        # Get actual spending for this category this month
        first_day = date(current_year, current_month, 1)
        today = date.today()

        actual_spent = (
            db.session.query(func.coalesce(func.sum(Transaction.amount), 0))
            .filter(
                Transaction.user_id == user_id,
                Transaction.category_id == budget.category_id,
                Transaction.transaction_type == "DEBIT",
                Transaction.transaction_date >= first_day,
                Transaction.transaction_date <= today
            )
            .scalar()
        ) or 0

        percentage = (float(actual_spent) / float(budget.monthly_limit) * 100) if budget.monthly_limit > 0 else 0

        budget_data.append({
            'budget_id': budget.budget_id,
            'category_name': category_name,
            'category_type': category_type,
            'monthly_limit': float(budget.monthly_limit),
            'actual_spent': float(actual_spent),
            'remaining': float(budget.monthly_limit - actual_spent),
            'percentage': round(percentage, 1),
            'status': 'danger' if percentage > 100 else ('warning' if percentage > 80 else 'success')
        })

    # Get categories that don't have budgets yet
    existing_category_ids = [b.category_id for b, _, _ in budgets]
    available_categories = (
        Category.query
        .filter(
            Category.category_type == "DEBIT",
            ~Category.category_id.in_(existing_category_ids) if existing_category_ids else True
        )
        .all()
    )

    return render_template(
        "budgets.html",
        budget_data=budget_data,
        available_categories=available_categories,
        current_month=current_month,
        current_year=current_year
    )


@budget_bp.route("/add-budget", methods=["POST"])
def add_budget():
    """Add a new budget for a category"""
    if "user_id" not in session:
        return redirect("/")

    try:
        user_id = session["user_id"]
        category_id = request.form.get("category_id")
        monthly_limit = request.form.get("monthly_limit")
        month = int(request.form.get("month", date.today().month))
        year = int(request.form.get("year", date.today().year))

        if not category_id or not monthly_limit:
            current_app.logger.warning(f"Missing budget data from user {session.get('username')}")
            return "Missing form data", 400

        # Check if budget already exists
        existing = Budget.query.filter_by(
            user_id=user_id,
            category_id=category_id,
            month=month,
            year=year
        ).first()

        if existing:
            current_app.logger.warning(f"Budget already exists for user {session.get('username')}")
            return redirect("/budgets")

        # Create new budget
        new_budget = Budget(
            user_id=user_id,
            category_id=int(category_id),
            monthly_limit=float(monthly_limit),
            month=month,
            year=year
        )

        db.session.add(new_budget)
        db.session.commit()

        current_app.logger.info(f"Budget added - User: {session.get('username')}, Category: {category_id}, Limit: {monthly_limit}")

        return redirect("/budgets")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Budget creation error - User: {session.get('username')}, Error: {str(e)}")
        return "Error creating budget", 500


@budget_bp.route("/update-budget/<int:budget_id>", methods=["POST"])
def update_budget(budget_id):
    """Update an existing budget"""
    if "user_id" not in session:
        return redirect("/")

    try:
        user_id = session["user_id"]
        budget = Budget.query.filter_by(budget_id=budget_id, user_id=user_id).first()

        if not budget:
            return "Budget not found", 404

        new_limit = request.form.get("monthly_limit")
        if new_limit:
            budget.monthly_limit = float(new_limit)
            db.session.commit()

            current_app.logger.info(f"Budget updated - User: {session.get('username')}, Budget ID: {budget_id}, New Limit: {new_limit}")

        return redirect("/budgets")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Budget update error - User: {session.get('username')}, Error: {str(e)}")
        return "Error updating budget", 500


@budget_bp.route("/delete-budget/<int:budget_id>")
def delete_budget(budget_id):
    """Delete a budget"""
    if "user_id" not in session:
        return redirect("/")

    try:
        user_id = session["user_id"]
        budget = Budget.query.filter_by(budget_id=budget_id, user_id=user_id).first()

        if not budget:
            return "Budget not found", 404

        db.session.delete(budget)
        db.session.commit()

        current_app.logger.info(f"Budget deleted - User: {session.get('username')}, Budget ID: {budget_id}")

        return redirect("/budgets")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Budget deletion error - User: {session.get('username')}, Error: {str(e)}")
        return "Error deleting budget", 500
