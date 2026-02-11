import time
import secrets
import logging
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, session, flash, url_for, current_app
from flask_mail import Message
from extensions import db, bcrypt, mail
from models import User
from logger_config import get_auth_logger

auth_bp = Blueprint("auth", __name__)

# Password reset token expiry time (30 minutes)
RESET_TOKEN_EXPIRY = 1800

# Get authentication logger
auth_logger = get_auth_logger()

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ip_address = request.remote_addr

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            session["user_id"] = user.user_id
            session["username"] = user.username   # ✅ STORE USERNAME

            auth_logger.info(f"Successful login - User: {username}, IP: {ip_address}")
            current_app.logger.info(f"User {username} logged in from {ip_address}")

            return redirect("/dashboard")

        auth_logger.warning(f"Failed login attempt - Username: {username}, IP: {ip_address}")
        flash("Invalid username or password.", "error")
        return render_template("login.html")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        ip_address = request.remote_addr

        # ✅ CHECK IF USERNAME EXISTS
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            auth_logger.warning(f"Registration failed - Username already exists: {username}, IP: {ip_address}")
            flash("Username already available. Please choose another.", "error")
            return redirect("/register")

        hashed_password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        user = User(
            full_name=request.form["full_name"],
            mobile_number=request.form["mobile_number"],
            email=email,
            username=username,
            password_hash=hashed_password
        )

        try:
            db.session.add(user)
            db.session.commit()

            auth_logger.info(f"New user registered - Username: {username}, Email: {email}, IP: {ip_address}")
            current_app.logger.info(f"New user account created: {username}")

            flash("Registration successful. Please login.", "success")
            return redirect("/")

        except Exception as e:
            db.session.rollback()
            auth_logger.error(f"Registration failed - Username: {username}, Error: {str(e)}")
            current_app.logger.error(f"Database error during registration: {str(e)}")
            flash("An error occurred during registration. Please try again.", "error")
            return redirect("/register")

    return render_template("register.html")


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate secure random token
            token = secrets.token_urlsafe(32)

            # Hash token before storing (security best practice)
            hashed_token = bcrypt.generate_password_hash(token).decode('utf-8')

            # Store hashed token and expiry in database
            user.reset_token = hashed_token
            user.reset_token_expiry = datetime.utcnow() + timedelta(seconds=RESET_TOKEN_EXPIRY)
            db.session.commit()

            # Send email with reset link
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            msg = Message(
                subject="Password Reset Request - FinanceTracker",
                recipients=[user.email]
            )
            msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #1a2b3c;">Password Reset Request</h2>
                        <p>Hello {user.full_name},</p>
                        <p>We received a request to reset your password for your FinanceTracker account.</p>
                        <p>Click the button below to reset your password:</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{reset_url}"
                               style="background-color: #27ae60; color: white; padding: 12px 30px;
                                      text-decoration: none; border-radius: 5px; display: inline-block;">
                                Reset Password
                            </a>
                        </div>
                        <p><strong>This link will expire in 30 minutes.</strong></p>
                        <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        <p style="font-size: 12px; color: #999;">
                            If the button doesn't work, copy and paste this link into your browser:<br>
                            <a href="{reset_url}" style="color: #27ae60;">{reset_url}</a>
                        </p>
                    </div>
                </body>
            </html>
            """

            try:
                mail.send(msg)
                auth_logger.info(f"Password reset email sent - Email: {email}, IP: {request.remote_addr}")
                current_app.logger.info(f"Password reset initiated for: {email}")
                flash("Password reset instructions have been sent to your email.", "success")
            except Exception as e:
                # Log error but don't reveal details to user
                auth_logger.error(f"Email sending failed - Email: {email}, Error: {str(e)}")
                current_app.logger.error(f"Email sending error: {str(e)}")
                flash("Password reset instructions have been sent to your email.", "success")
        else:
            # Security: Always show success message even if email doesn't exist
            auth_logger.warning(f"Password reset attempt for non-existent email: {email}, IP: {request.remote_addr}")
            flash("Password reset instructions have been sent to your email.", "success")

        return redirect(url_for('auth.forgot_password'))

    return render_template("forgot_password.html")


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # Find user with matching token that hasn't expired
    users = User.query.filter(User.reset_token.isnot(None)).all()

    user = None
    for u in users:
        # Check if token matches (compare hashed)
        if bcrypt.check_password_hash(u.reset_token, token):
            # Check if token hasn't expired
            if u.reset_token_expiry and u.reset_token_expiry > datetime.utcnow():
                user = u
                break

    if not user:
        auth_logger.warning(f"Invalid/expired password reset token attempt - IP: {request.remote_addr}")
        flash("Invalid or expired password reset link. Please request a new one.", "error")
        return redirect(url_for('auth.forgot_password'))

    if request.method == "POST":
        new_password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Validations
        if not new_password or not confirm_password:
            flash("Both password fields are required.", "error")
            return render_template("reset_password.html", email=user.email)

        if len(new_password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return render_template("reset_password.html", email=user.email)

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("reset_password.html", email=user.email)

        # Update password
        user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # Clear/invalidate the reset token (one-time use)
        user.reset_token = None
        user.reset_token_expiry = None
        db.session.commit()

        auth_logger.info(f"Password reset completed - User: {user.username}, Email: {user.email}, IP: {request.remote_addr}")
        current_app.logger.info(f"Password successfully reset for user: {user.username}")

        flash("Password reset successful! You can now login with your new password.", "success")
        return redirect(url_for('auth.login'))

    return render_template("reset_password.html", email=user.email)


@auth_bp.route("/logout")
def logout():
    username = session.get("username", "Unknown")
    ip_address = request.remote_addr

    auth_logger.info(f"User logged out - User: {username}, IP: {ip_address}")
    current_app.logger.info(f"User {username} logged out")

    session.clear()
    return redirect("/")
