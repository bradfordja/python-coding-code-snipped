from datetime import datetime, timedelta, timezone

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.schemas.auth import TokenPayload


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Convert a plain-text password into a secure hash."""
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Compare a plain password with its stored hash."""
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(username: str) -> str:
    now = datetime.now(timezone.utc)

    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": username,
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={
                "require": ["sub", "exp"],
            },
        )

        return TokenPayload.model_validate(payload)

    except ExpiredSignatureError as exc:
        raise AuthenticationError(
            message="The access token has expired",
            code="TOKEN_EXPIRED",
        ) from exc

    except (InvalidTokenError, ValueError) as exc:
        raise AuthenticationError(
            message="The access token is invalid",
            code="INVALID_TOKEN",
        ) from exc