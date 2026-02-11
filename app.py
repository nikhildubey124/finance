from flask import Flask, session
from config import Config
from extensions import db, bcrypt, jwt, mail
from logger_config import setup_logger

def create_app():
    app = Flask("finance_app")
    app.config.from_object(Config)

    # Initialize logging
    setup_logger(app)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.transactions import txn_bp
    from routes.dashboard import dashboard_bp
    from routes.budgets import budget_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(txn_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(budget_bp)

    # ✅ Context processor MUST be inside create_app
    @app.context_processor
    def inject_user():
        return dict(active_user=session.get("username"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    