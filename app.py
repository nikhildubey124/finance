from flask import Flask, session
from config import Config
from extensions import db, bcrypt, jwt, mail, cache, compress
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

    # Performance optimizations
    cache.init_app(app)      # Cache frequently accessed data
    compress.init_app(app)   # Compress HTTP responses (gzip)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.transactions import txn_bp
    from routes.dashboard import dashboard_bp
    from routes.budgets import budget_bp
    from routes.categories import category_bp
    from routes.bulk_upload import bulk_upload_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(txn_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(budget_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(bulk_upload_bp)

    # Error handlers for stability
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # Rollback any failed transactions
        app.logger.error(f"Internal server error: {str(error)}")
        return {"error": "Internal server error"}, 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        db.session.rollback()
        app.logger.error(f"Unhandled exception: {str(error)}")
        return {"error": "An unexpected error occurred"}, 500

    # Context processor
    @app.context_processor
    def inject_user():
        return dict(active_user=session.get("username"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    