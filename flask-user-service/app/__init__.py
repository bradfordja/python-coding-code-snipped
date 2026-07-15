import os

from dotenv import load_dotenv
from flask import Flask

from app.core.config import CONFIG_BY_NAME
from app.core.error_handlers import register_error_handlers
from app.extensions import db, jwt


def create_app(config_name: str | None = None) -> Flask:
    """
    Application factory.

    It creates and configures a new Flask application instance.
    This makes testing and running multiple environments easier.
    """

    load_dotenv()

    environment = config_name or os.getenv(
        "FLASK_ENV",
        "development",
    )

    app = Flask(__name__)

    config_class = CONFIG_BY_NAME.get(
        environment,
        CONFIG_BY_NAME["development"],
    )

    app.config.from_object(config_class)

    # Initialize Flask extensions.
    db.init_app(app)
    jwt.init_app(app)

    # Register routes.
    register_blueprints(app)

    # Register centralized exception handlers.
    register_error_handlers(app)

    # Register JWT-specific error handlers.
    register_jwt_handlers(jwt)

    return app


def register_blueprints(app: Flask) -> None:
    from app.routes.auth_routes import auth_blueprint
    from app.routes.health_routes import health_blueprint
    from app.routes.user_routes import user_blueprint

    app.register_blueprint(
        health_blueprint,
        url_prefix="/api/v1",
    )

    app.register_blueprint(
        auth_blueprint,
        url_prefix="/api/v1/auth",
    )

    app.register_blueprint(
        user_blueprint,
        url_prefix="/api/v1/users",
    )


def register_jwt_handlers(jwt_manager: JWTManager) -> None:
    """
    Return consistent JSON errors for JWT failures.
    """

    @jwt_manager.unauthorized_loader
    def missing_token(reason: str):
        return {
            "error": {
                "code": "MISSING_TOKEN",
                "message": reason,
                "details": None,
            }
        }, 401

    @jwt_manager.invalid_token_loader
    def invalid_token(reason: str):
        return {
            "error": {
                "code": "INVALID_TOKEN",
                "message": reason,
                "details": None,
            }
        }, 401

    @jwt_manager.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return {
            "error": {
                "code": "TOKEN_EXPIRED",
                "message": "The access token has expired",
                "details": None,
            }
        }, 401

    @jwt_manager.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        return {
            "error": {
                "code": "TOKEN_REVOKED",
                "message": "The access token has been revoked",
                "details": None,
            }
        }, 401