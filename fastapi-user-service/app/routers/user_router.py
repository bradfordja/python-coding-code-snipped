from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.dependencies.auth import require_permission
from app.dependencies.repositories import get_user_repository
from app.models.user import Permission, User
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> UserService:
    return UserService(repository)


UserServiceDependency = Annotated[
    UserService,
    Depends(get_user_service),
]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: UserCreate,
    service: UserServiceDependency,
    authenticated_user: Annotated[
        User,
        Depends(
            require_permission(Permission.USER_CREATE)
        ),
    ],
) -> UserResponse:
    user = service.create_user(request)

    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    service: UserServiceDependency,
    authenticated_user: Annotated[
        User,
        Depends(
            require_permission(Permission.USER_READ)
        ),
    ],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
) -> list[UserResponse]:
    users = service.get_all_users(skip, limit)

    return [
        UserResponse.model_validate(user)
        for user in users
    ]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    service: UserServiceDependency,
    authenticated_user: Annotated[
        User,
        Depends(
            require_permission(Permission.USER_READ)
        ),
    ],
) -> UserResponse:
    user = service.get_user(user_id)

    return UserResponse.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    request: UserUpdate,
    service: UserServiceDependency,
    authenticated_user: Annotated[
        User,
        Depends(
            require_permission(Permission.USER_UPDATE)
        ),
    ],
) -> UserResponse:
    user = service.update_user(user_id, request)

    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_id: int,
    service: UserServiceDependency,
    authenticated_user: Annotated[
        User,
        Depends(
            require_permission(Permission.USER_DELETE)
        ),
    ],
) -> None:
    service.delete_user(
        user_id=user_id,
        authenticated_user=authenticated_user,
    )