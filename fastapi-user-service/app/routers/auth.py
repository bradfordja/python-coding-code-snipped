from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
)
from app.core.security import decode_access_token
from app.dependencies.repositories import get_user_repository
from app.models.user import (
    Permission,
    ROLE_PERMISSIONS,
    User,
)
from app.repositories.user_repository import UserRepository


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> User:
    if credentials is None:
        raise AuthenticationError(
            message="A bearer token is required",
            code="MISSING_TOKEN",
        )

    if credentials.scheme.lower() != "bearer":
        raise AuthenticationError(
            message="The authentication scheme must be Bearer",
            code="INVALID_AUTHENTICATION_SCHEME",
        )

    payload = decode_access_token(
        credentials.credentials
    )

    user = user_repository.find_by_username(payload.sub)

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

    return user


CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]


def require_permission(
    permission: Permission,
) -> Callable:
    """
    Dependency factory.

    Example:
        Depends(require_permission(Permission.USER_CREATE))
    """

    def check_permission(
        current_user: CurrentUser,
    ) -> User:
        available_permissions = ROLE_PERMISSIONS.get(
            current_user.role,
            set(),
        )

        if permission not in available_permissions:
            raise AuthorizationError(
                message=(
                    f"Permission '{permission.value}' is required"
                )
            )

        return current_user

    return check_permission