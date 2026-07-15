from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError as MarshmallowValidationError

from app.core.exceptions import (
    AuthenticationError,
    ValidationError,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import LoginSchema
from app.services.auth_service import AuthService


auth_blueprint = Blueprint(
    "authentication",
    __name__,
)

login_schema = LoginSchema()


@auth_blueprint.post("/login")
def login():
    try:
        data = login_schema.load(
            request.get_json(silent=True) or {}
        )
    except MarshmallowValidationError as error:
        raise ValidationError(error.messages) from error

    result = AuthService.login(
        username=data["username"],
        password=data["password"],
    )

    return jsonify(result), 200


@auth_blueprint.get("/me")
@jwt_required()
def get_current_profile():
    identity = get_jwt_identity()

    try:
        user_id = int(identity)
    except (TypeError, ValueError) as error:
        raise AuthenticationError(
            "Invalid JWT user identity"
        ) from error

    user = UserRepository.find_by_id(user_id)

    if user is None:
        raise AuthenticationError(
            message="The authenticated user does not exist",
            code="USER_NOT_FOUND",
        )

    if user.disabled:
        raise AuthenticationError(
            message="The authenticated user is disabled",
            code="USER_DISABLED",
        )

    return jsonify(user.to_dict()), 200