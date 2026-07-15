from flask_jwt_extended import create_access_token

from app.core.exceptions import AuthenticationError
from app.core.security import verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    @staticmethod
    def login(
        username: str,
        password: str,
    ) -> dict:
        user = UserRepository.find_by_username(username)

        if user is None or not verify_password(
            password,
            user.password_hash,
        ):
            raise AuthenticationError(
                message="Incorrect username or password",
                code="INVALID_CREDENTIALS",
            )

        if user.disabled:
            raise AuthenticationError(
                message="The user account is disabled",
                code="USER_DISABLED",
            )

        access_token = create_access_token(
            # JWT subject should use a string.
            identity=str(user.id),

            additional_claims={
                "username": user.username,
                "role": user.role,
            },
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user.to_dict(),
        }