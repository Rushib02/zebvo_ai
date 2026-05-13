from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from datetime import datetime

from app.config.config import config_by_name
from app.database.mongodb import db
from app.utils.logger import request_logger, error_logger

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize Extensions
    CORS(app)
    JWTManager(app)
    db.init_app(app)

    # Register Blueprints
    from app.routes.health import health_bp
    from app.routes.auth import auth_bp
    from app.routes.project import project_bp

    app.register_blueprint(health_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(project_bp, url_prefix='/api/projects')

    # Centralized Error Handling
    register_error_handlers(app)
    register_jwt_handlers(app)

    # Request Lifecycle Hooks
    register_request_hooks(app)

    return app

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found", "status_code": 404}), 404

    @app.errorhandler(500)
    def internal_error(error):
        error_logger.error(f"Internal Server Error: {str(error)}", extra={
            "path": request.path,
            "method": request.method
        })
        return jsonify({"error": "Internal server error", "status_code": 500}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        error_logger.exception(f"Unhandled Exception: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "status_code": 500}), 500

def register_jwt_handlers(app):
    jwt = app.extensions['flask-jwt-extended']

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "The token has expired", "status_code": 401}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"error": "Signature verification failed", "status_code": 401}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"error": "Request does not contain an access token", "status_code": 401}), 401

def register_request_hooks(app):
    @app.before_request
    def log_request_info():
        request_logger.info("Request received", extra={
            "method": request.method,
            "url": request.url,
            "remote_addr": request.remote_addr,
            "headers": dict(request.headers)
        })

    @app.after_request
    def log_response_info(response):
        request_logger.info("Response sent", extra={
            "method": request.method,
            "url": request.url,
            "status_code": response.status_code
        })
        return response
