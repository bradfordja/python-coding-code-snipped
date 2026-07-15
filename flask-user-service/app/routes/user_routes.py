from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError

from app.core.exceptions import ValidationError
from app.core.security import permission_required
from app.models.user import Permission, User
from app.schemas.user_schema import (
    UserCreateSchema,
    UserUpdateSchema,
)
from app.services.user_service import UserService


user_blueprint = Blueprint(
    "users",
    __name__,
)

create_schema = UserCreateSchema()
update_schema = UserUpdateSchema()


@user_blueprint.get("")
@permission_required(Permission.USER_READ)
def get_users(current_user: User):
    page = request.args.get(
        "page",
        default=1,
        type=int,
    )

    page_size = request.args.get(
        "page_size",
        default=20,
        type=int,
    )

    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)

    result = UserService.get_users(
        page=page,
        page_size=page_size,
    )

    return jsonify(result), 200


@user_blueprint.get("/<int:user_id>")
@permission_required(Permission.USER_READ)
def get_user(
    user_id: int,
    current_user: User,
):
    user = UserService.get_user(user_id)

    return jsonify(user.to_dict()), 200


@user_blueprint.post("")
@permission_required(Permission.USER_CREATE)
def create_user(current_user: User):
    try:
        data = create_schema.load(
            request.get_json(silent=True) or {}
        )
    except MarshmallowValidationError as error:
        raise ValidationError(error.messages) from error

    user = UserService.create_user(data)

    return jsonify(user.to_dict()), 201


@user_blueprint.patch("/<int:user_id>")
@permission_required(Permission.USER_UPDATE)
def update_user(
    user_id: int,
    current_user: User,
):
    try:
        data = update_schema.load(
            request.get_json(silent=True) or {}
        )
    except MarshmallowValidationError as error:
        raise ValidationError(error.messages) from error

    user = UserService.update_user(
        user_id=user_id,
        data=data,
    )

    return jsonify(user.to_dict()), 200


@user_blueprint.delete("/<int:user_id>")
@permission_required(Permission.USER_DELETE)
def delete_user(
    user_id: int,
    current_user: User,
):
    UserService.delete_user(
        user_id=user_id,
        current_user=current_user,
    )

    return "", 204