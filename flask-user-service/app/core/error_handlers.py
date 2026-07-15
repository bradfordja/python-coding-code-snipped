import logging

from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import ApplicationError
from app.extensions import db


logger = logging.getLogger(__name__)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApplicationError)
    def handle_application_error(error: ApplicationError):
        return jsonify(
            {
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "details": error.details,
                }
            }
        ), error.status_code

    @app.errorhandler(404)
    def handle_route_not_found(error):
        return jsonify(
            {
                "error": {
                    "code": "ROUTE_NOT_FOUND",
                    "message": "The requested endpoint does not exist",
                    "details": None,
                }
            }
        ), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify(
            {
                "error": {
                    "code": "METHOD_NOT_ALLOWED",
                    "message": "The HTTP method is not allowed",
                    "details": None,
                }
            }
        ), 405

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error: SQLAlchemyError):
        db.session.rollback()

        logger.exception("Database error")

        return jsonify(
            {
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "A database operation failed",
                    "details": None,
                }
            }
        ), 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        logger.exception("Unexpected application error")

        return jsonify(
            {
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": None,
                }
            }
        ), 500