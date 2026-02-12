from flask import Blueprint, render_template, request, redirect, session, current_app, send_file, flash
from extensions import db
from models import Transaction, Category
from datetime import datetime, date, timedelta
from werkzeug.utils import secure_filename
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from io import BytesIO
import os

bulk_upload_bp = Blueprint("bulk_upload", __name__)

# Configuration
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_previous_month_range():
    """Get first and last day of previous month"""
    today = date.today()
    first_day_current_month = today.replace(day=1)
    last_day_previous_month = first_day_current_month - timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    return first_day_previous_month, last_day_previous_month


@bulk_upload_bp.route("/bulk-upload")
def bulk_upload():
    """Bulk upload page"""
    if "user_id" not in session:
        return redirect("/")

    first_day, last_day = get_previous_month_range()

    return render_template(
        "bulk_upload.html",
        previous_month=first_day.strftime("%B %Y"),
        date_range=f"{first_day.strftime('%Y-%m-%d')} to {last_day.strftime('%Y-%m-%d')}",
        active_user=session.get("username", "Guest")
    )


@bulk_upload_bp.route("/download-template/<file_type>")
def download_template(file_type):
    """Generate and download Excel or CSV template"""
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    # Get user's categories for reference
    categories = Category.query.filter(
        db.or_(Category.user_id == None, Category.user_id == user_id)
    ).order_by(Category.category_type, Category.category_name).all()

    # Get previous month date range
    first_day, last_day = get_previous_month_range()

    # Create DataFrame with template structure
    template_data = {
        'Transaction Date (YYYY-MM-DD)': [
            first_day.strftime('%Y-%m-%d'),
            '',  # Empty row for user to fill
        ],
        'Transaction Type (CREDIT/DEBIT)': [
            'DEBIT',
            '',
        ],
        'Amount': [
            '1000.00',
            '',
        ],
        'Category Name': [
            categories[0].category_name if categories else 'Food',
            '',
        ]
    }

    df = pd.DataFrame(template_data)

    if file_type == 'excel':
        # Create Excel file with formatting
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Transactions')

            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Transactions']

            # Style header row
            header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            header_font = Font(color='FFFFFF', bold=True)

            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

            # Add instructions sheet
            instructions_data = {
                'Instructions': [
                    'HOW TO USE THIS TEMPLATE:',
                    '',
                    '1. Fill in your transaction data in the "Transactions" sheet',
                    '2. Transaction Date must be in YYYY-MM-DD format (e.g., 2024-01-15)',
                    f'3. Date must be between {first_day.strftime("%Y-%m-%d")} and {last_day.strftime("%Y-%m-%d")}',
                    '4. Transaction Type must be either CREDIT or DEBIT',
                    '5. Amount must be a positive number (e.g., 1000.00)',
                    '6. Category Name must match one of your existing categories',
                    '',
                    'AVAILABLE CATEGORIES:',
                ] + [f'  - {cat.category_name} ({cat.category_type})' for cat in categories[:20]]
            }

            instructions_df = pd.DataFrame(instructions_data)
            instructions_df.to_excel(writer, index=False, sheet_name='Instructions')

        output.seek(0)

        filename = f'transaction_template_{first_day.strftime("%Y_%m")}.xlsx'

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    elif file_type == 'csv':
        # Create CSV file
        output = BytesIO()

        # Add instructions as comments
        instructions = [
            f"# Transaction Upload Template for {first_day.strftime('%B %Y')}",
            f"# Date Range: {first_day.strftime('%Y-%m-%d')} to {last_day.strftime('%Y-%m-%d')}",
            "# Format: Transaction Date (YYYY-MM-DD), Transaction Type (CREDIT/DEBIT), Amount, Category Name",
            "# Example: 2024-01-15, DEBIT, 1000.00, Food",
            f"# Available Categories: {', '.join([cat.category_name for cat in categories[:10]])}",
            "",
        ]

        # Write instructions
        for instruction in instructions:
            output.write((instruction + '\n').encode('utf-8'))

        # Write data
        df.to_csv(output, index=False)
        output.seek(0)

        filename = f'transaction_template_{first_day.strftime("%Y_%m")}.csv'

        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )


@bulk_upload_bp.route("/upload-transactions", methods=["POST"])
def upload_transactions():
    """Process uploaded transaction file"""
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]

    # Check if file was uploaded
    if 'file' not in request.files:
        flash("No file uploaded. Please select a file.", "error")
        return redirect("/bulk-upload")

    file = request.files['file']

    if file.filename == '':
        flash("No file selected. Please choose a file to upload.", "error")
        return redirect("/bulk-upload")

    if not allowed_file(file.filename):
        flash("Invalid file format. Please upload an Excel (.xlsx, .xls) or CSV (.csv) file.", "error")
        return redirect("/bulk-upload")

    try:
        # Read file based on extension
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()

        if file_ext == 'csv':
            # Read CSV, skip comment lines
            df = pd.read_csv(file, comment='#')
        else:
            # Read Excel
            df = pd.read_excel(file, sheet_name='Transactions')

        # Validate and process data
        first_day, last_day = get_previous_month_range()

        validation_errors = []
        valid_records = []
        duplicate_count = 0

        # Get user's categories for validation
        user_categories = {
            cat.category_name.lower(): cat
            for cat in Category.query.filter(
                db.or_(Category.user_id == None, Category.user_id == user_id)
            ).all()
        }

        for index, row in df.iterrows():
            row_num = index + 2  # +2 because index starts at 0 and header is row 1
            errors = []

            # Skip empty rows
            if row.isna().all():
                continue

            # Validate Transaction Date
            try:
                if pd.isna(row['Transaction Date (YYYY-MM-DD)']):
                    errors.append("Transaction Date is required")
                else:
                    txn_date_str = str(row['Transaction Date (YYYY-MM-DD)']).strip()
                    # Handle different date formats
                    for date_format in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
                        try:
                            txn_date = datetime.strptime(txn_date_str, date_format).date()
                            break
                        except ValueError:
                            continue
                    else:
                        errors.append("Invalid date format. Use YYYY-MM-DD (e.g., 2024-01-15)")
                        txn_date = None

                    # Validate date is in previous month
                    if txn_date and not (first_day <= txn_date <= last_day):
                        errors.append(f"Date must be between {first_day} and {last_day}")

            except Exception as e:
                errors.append(f"Date error: {str(e)}")
                txn_date = None

            # Validate Transaction Type
            if pd.isna(row['Transaction Type (CREDIT/DEBIT)']):
                errors.append("Transaction Type is required")
                txn_type = None
            else:
                txn_type = str(row['Transaction Type (CREDIT/DEBIT)']).strip().upper()
                if txn_type not in ['CREDIT', 'DEBIT']:
                    errors.append("Transaction Type must be CREDIT or DEBIT")

            # Validate Amount
            try:
                if pd.isna(row['Amount']):
                    errors.append("Amount is required")
                    amount = None
                else:
                    amount = float(row['Amount'])
                    if amount <= 0:
                        errors.append("Amount must be greater than 0")
            except ValueError:
                errors.append("Amount must be a valid number")
                amount = None

            # Validate Category
            if pd.isna(row['Category Name']):
                errors.append("Category Name is required")
                category = None
            else:
                category_name = str(row['Category Name']).strip()
                category = user_categories.get(category_name.lower())

                if not category:
                    errors.append(f"Category '{category_name}' not found. Please use an existing category.")

            # Check for duplicates
            if txn_date and amount and category and not errors:
                duplicate = Transaction.query.filter_by(
                    user_id=user_id,
                    transaction_date=txn_date,
                    amount=amount,
                    category_id=category.category_id
                ).first()

                if duplicate:
                    errors.append("Duplicate transaction already exists in database")
                    duplicate_count += 1

            if errors:
                validation_errors.append({
                    'row': row_num,
                    'date': txn_date_str if 'txn_date_str' in locals() else str(row['Transaction Date (YYYY-MM-DD)']),
                    'type': txn_type if txn_type else str(row['Transaction Type (CREDIT/DEBIT)']),
                    'amount': amount if amount else str(row['Amount']),
                    'category': category_name if 'category_name' in locals() else str(row['Category Name']),
                    'errors': ', '.join(errors)
                })
            else:
                valid_records.append({
                    'date': txn_date,
                    'type': txn_type,
                    'amount': amount,
                    'category_id': category.category_id
                })

        # If there are validation errors, show them
        if validation_errors:
            return render_template(
                "upload_results.html",
                success=False,
                total_rows=len(df),
                valid_count=len(valid_records),
                error_count=len(validation_errors),
                duplicate_count=duplicate_count,
                errors=validation_errors,
                active_user=session.get("username", "Guest")
            )

        # Import valid records
        imported_count = 0
        for record in valid_records:
            transaction = Transaction(
                user_id=user_id,
                transaction_type=record['type'],
                amount=record['amount'],
                category_id=record['category_id'],
                transaction_date=record['date']
            )
            db.session.add(transaction)
            imported_count += 1

        db.session.commit()

        current_app.logger.info(f"Bulk upload completed - User: {session.get('username')}, Imported: {imported_count}")

        flash(f"Successfully imported {imported_count} transactions!", "success")

        return render_template(
            "upload_results.html",
            success=True,
            total_rows=len(df),
            valid_count=len(valid_records),
            imported_count=imported_count,
            error_count=0,
            duplicate_count=duplicate_count,
            active_user=session.get("username", "Guest")
        )

    except Exception as e:
        current_app.logger.error(f"Bulk upload error - User: {session.get('username')}, Error: {str(e)}")
        flash(f"Error processing file: {str(e)}", "error")
        return redirect("/bulk-upload")
