from flask import Blueprint, render_template, request, redirect, session, current_app, flash
from extensions import db
from models import Category
from sqlalchemy import or_

category_bp = Blueprint("categories", __name__)


@category_bp.route("/categories")
def categories():
    """Category Management - List all categories"""
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    # Get system categories (available to all users) and user's custom categories
    all_categories = Category.query.filter(
        or_(Category.user_id == None, Category.user_id == user_id)
    ).order_by(Category.category_type, Category.category_name).all()

    # Organize categories by type
    credit_categories = [c for c in all_categories if c.category_type == "CREDIT"]
    debit_categories = [c for c in all_categories if c.category_type == "DEBIT"]

    return render_template(
        "categories.html",
        credit_categories=credit_categories,
        debit_categories=debit_categories,
        active_user=session.get("username", "Guest")
    )


@category_bp.route("/add-category", methods=["GET", "POST"])
def add_category():
    """Add a new custom category"""
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        try:
            user_id = session["user_id"]
            category_name = request.form.get("category_name")
            category_type = request.form.get("category_type")
            icon = request.form.get("icon", "").strip()
            color = request.form.get("color", "").strip()
            parent_id = request.form.get("parent_category_id")

            # Validation
            if not category_name or not category_type:
                flash("Category name and type are required.", "error")
                return redirect("/add-category")

            # Create category
            category = Category(
                category_name=category_name,
                category_type=category_type.upper(),
                user_id=user_id,
                icon=icon if icon else None,
                color=color if color else None,
                parent_category_id=int(parent_id) if parent_id and parent_id != "" else None
            )

            db.session.add(category)
            db.session.commit()

            current_app.logger.info(f"Category created - Name: {category_name}, Type: {category_type}, User: {session.get('username')}")

            flash(f"Category '{category_name}' created successfully!", "success")
            return redirect("/categories")

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Category creation error - User: {session.get('username')}, Error: {str(e)}")
            flash("Error creating category. Please try again.", "error")
            return redirect("/add-category")

    # GET request - show form
    user_id = session["user_id"]

    # Get user's categories for parent selection
    parent_categories = Category.query.filter(
        or_(Category.user_id == None, Category.user_id == user_id),
        Category.parent_category_id == None  # Only top-level categories can be parents
    ).order_by(Category.category_type, Category.category_name).all()

    return render_template(
        "add_category.html",
        parent_categories=parent_categories,
        active_user=session.get("username", "Guest")
    )


@category_bp.route("/edit-category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """Edit an existing category"""
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    # Get category - must be user's own category
    category = Category.query.filter_by(
        category_id=category_id,
        user_id=user_id
    ).first()

    if not category:
        flash("Category not found or you don't have permission to edit it.", "error")
        return redirect("/categories")

    if request.method == "POST":
        try:
            category.category_name = request.form.get("category_name")
            category.category_type = request.form.get("category_type").upper()
            category.icon = request.form.get("icon", "").strip() or None
            category.color = request.form.get("color", "").strip() or None

            parent_id = request.form.get("parent_category_id")
            category.parent_category_id = int(parent_id) if parent_id and parent_id != "" else None

            db.session.commit()

            current_app.logger.info(f"Category updated - ID: {category_id}, User: {session.get('username')}")

            flash(f"Category '{category.category_name}' updated successfully!", "success")
            return redirect("/categories")

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Category update error - ID: {category_id}, Error: {str(e)}")
            flash("Error updating category. Please try again.", "error")
            return redirect(f"/edit-category/{category_id}")

    # GET request - show form
    parent_categories = Category.query.filter(
        or_(Category.user_id == None, Category.user_id == user_id),
        Category.parent_category_id == None,
        Category.category_id != category_id  # Can't be its own parent
    ).order_by(Category.category_type, Category.category_name).all()

    return render_template(
        "edit_category.html",
        category=category,
        parent_categories=parent_categories,
        active_user=session.get("username", "Guest")
    )


@category_bp.route("/delete-category/<int:category_id>")
def delete_category(category_id):
    """Delete a custom category"""
    if "user_id" not in session:
        return redirect("/")

    try:
        user_id = session["user_id"]

        # Get category - must be user's own category
        category = Category.query.filter_by(
            category_id=category_id,
            user_id=user_id
        ).first()

        if not category:
            flash("Category not found or you don't have permission to delete it.", "error")
            return redirect("/categories")

        # Check if category is being used in transactions
        if category.transactions:
            flash(f"Cannot delete '{category.category_name}' because it has associated transactions.", "error")
            return redirect("/categories")

        category_name = category.category_name
        db.session.delete(category)
        db.session.commit()

        current_app.logger.info(f"Category deleted - ID: {category_id}, Name: {category_name}, User: {session.get('username')}")

        flash(f"Category '{category_name}' deleted successfully!", "success")
        return redirect("/categories")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Category deletion error - ID: {category_id}, Error: {str(e)}")
        flash("Error deleting category. Please try again.", "error")
        return redirect("/categories")
