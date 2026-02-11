"""
Logging configuration for FinanceTracker application
Configures file and console logging with rotation
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logger(app):
    """
    Configure application logging

    Creates three log files:
    - app.log: All application logs (INFO and above)
    - error.log: Only errors and critical issues
    - auth.log: Authentication and security events
    """

    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Set logging level based on environment
    if app.config['DEBUG']:
        app.logger.setLevel(logging.DEBUG)
    else:
        app.logger.setLevel(logging.INFO)

    # Remove default handlers
    app.logger.handlers = []

    # Format for log messages
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    # Main application log file (rotating, max 10MB, keep 10 backups)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    # Error log file (only errors and critical)
    error_handler = RotatingFileHandler(
        'logs/error.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    app.logger.addHandler(error_handler)

    # Authentication log file (security events)
    auth_handler = RotatingFileHandler(
        'logs/auth.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=10
    )
    auth_handler.setLevel(logging.INFO)
    auth_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    auth_handler.setFormatter(auth_formatter)

    # Create separate logger for auth events
    auth_logger = logging.getLogger('auth')
    auth_logger.setLevel(logging.INFO)
    auth_logger.addHandler(auth_handler)
    auth_logger.addHandler(console_handler)

    app.logger.info('='*60)
    app.logger.info('FinanceTracker application started')
    app.logger.info(f'Environment: {"Development" if app.config["DEBUG"] else "Production"}')
    app.logger.info('='*60)

    # Log HTTP requests
    @app.after_request
    def log_request(response):
        from flask import request
        app.logger.info(f'{request.method} {request.path} - Status: {response.status_code} - IP: {request.remote_addr}')
        return response

    return app.logger

def get_auth_logger():
    """Get the authentication logger"""
    return logging.getLogger('auth')
