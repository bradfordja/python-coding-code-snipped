from flask import Blueprint, jsonify
from sqlalchemy import text

from app.extensions import db


health_blueprint = Blueprint(
    "health",
    __name__,
)


@health_blueprint.get("/health")
def health():
    return jsonify(
        {
            "status": "UP",
            "service": "user-service",
        }
    ), 200


@health_blueprint.get("/health/ready")
def readiness():
    try:
        db.session.execute(text("SELECT 1"))

        return jsonify(
            {
                "status": "READY",
                "database": "UP",
            }
        ), 200

    except Exception:
        return jsonify(
            {
                "status": "NOT_READY",
                "database": "DOWN",
            }
        ), 503