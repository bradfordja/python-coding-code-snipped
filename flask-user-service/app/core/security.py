from functools import wraps
from typing import Callable

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
)
from app.models.user import (
    Permission,
    ROLE_PERMISSIONS,
)
from app.repositories.user_repository import UserRepository


def hash_password(password: str) -> str:
    return generate_password_hash(
        password,
        method="scrypt",
    )


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    return check_password_hash(
        password_hash,
        password,
    )


def permission_required(
    permission: Permission,
) -> Callable:
    """
    Protect a route and verify the user has a permission.

    Authentication:
        Is the token valid?

    Authorization:
        Does this authenticated user have access?
    """

    def decorator(route_function: Callable) -> Callable:
        @wraps(route_function)
        @jwt_required()
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()

            if identity is None:
                raise AuthenticationError(
                    "The token does not contain a user identity"
                )

            try:
                user_id = int(identity)
            except (TypeError, ValueError) as error:
                raise AuthenticationError(
                    "The token contains an invalid user identity"
                ) from error

            user = UserRepository.find_by_id(user_id)

            if user is None:
                raise AuthenticationError(
                    message="The authenticated user no longer exists",
                    code="USER_NOT_FOUND",
                )

            if user.disabled:
                raise AuthenticationError(
                    message="The authenticated user is disabled",
                    code="USER_DISABLED",
                )

            permissions = ROLE_PERMISSIONS.get(
                user.get_role(),
                set(),
            )

            if permission not in permissions:
                raise AuthorizationError(
                    f"Permission '{permission.value}' is required"
                )

            # Pass the authenticated user into the route.
            return route_function(
                *args,
                current_user=user,
                **kwargs,
            )

        return wrapper

    return decorator