from app.core.exceptions import (
    ConflictError,
    NotFoundError,
)
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def get_users(
        page: int,
        page_size: int,
    ) -> dict:
        users, total = UserRepository.find_all(
            page=page,
            page_size=page_size,
        )

        return {
            "items": [user.to_dict() for user in users],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (
                    (total + page_size - 1) // page_size
                    if total
                    else 0
                ),
            },
        }

    @staticmethod
    def get_user(user_id: int) -> User:
        user = UserRepository.find_by_id(user_id)

        if user is None:
            raise NotFoundError("User", user_id)

        return user

    @staticmethod
    def create_user(data: dict) -> User:
        username = data["username"].strip()
        email = data["email"].strip().lower()

        if UserRepository.find_by_username(username):
            raise ConflictError(
                f"Username '{username}' already exists"
            )

        if UserRepository.find_by_email(email):
            raise ConflictError(
                f"Email '{email}' already exists"
            )

        user = User(
            username=username,
            email=email,
            full_name=data["full_name"].strip(),
            password_hash=hash_password(data["password"]),
            role=data["role"],
            disabled=False,
        )

        return UserRepository.create(user)

    @staticmethod
    def update_user(
        user_id: int,
        data: dict,
    ) -> User:
        user = UserService.get_user(user_id)

        if "email" in data:
            email = data["email"].strip().lower()
            existing = UserRepository.find_by_email(email)

            if existing and existing.id != user.id:
                raise ConflictError(
                    f"Email '{email}' already exists"
                )

            user.email = email

        if "full_name" in data:
            user.full_name = data["full_name"].strip()

        if "password" in data:
            user.password_hash = hash_password(
                data["password"]
            )

        if "role" in data:
            user.role = data["role"]

        if "disabled" in data:
            user.disabled = data["disabled"]

        return UserRepository.update(user)

    @staticmethod
    def delete_user(
        user_id: int,
        current_user: User,
    ) -> None:
        user = UserService.get_user(user_id)

        if user.id == current_user.id:
            raise ConflictError(
                "You cannot delete your own authenticated account"
            )

        UserRepository.delete(user)