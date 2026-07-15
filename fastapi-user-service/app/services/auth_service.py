from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(
        self,
        username: str,
        password: str,
    ) -> TokenResponse:
        user = self.user_repository.find_by_username(username)

        if user is None or not verify_password(
            password,
            user.hashed_password,
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

        access_token = create_access_token(user.username)

        return TokenResponse(
            access_token=access_token,
            expires_in=(
                settings.access_token_expire_minutes * 60
            ),
        )