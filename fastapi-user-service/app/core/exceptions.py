from typing import Any

from fastapi import status


class ApplicationError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details

        super().__init__(message)


class AuthenticationError(ApplicationError):
    def __init__(
        self,
        message: str = "Authentication failed",
        code: str = "AUTHENTICATION_FAILED",
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=code,
            message=message,
        )


class AuthorizationError(ApplicationError):
    def __init__(
        self,
        message: str = "You do not have permission",
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="ACCESS_DENIED",
            message=message,
        )


class NotFoundError(ApplicationError):
    def __init__(self, resource: str, resource_id: object):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=f"{resource} was not found",
            details={
                "resource": resource,
                "id": resource_id,
            },
        )


class ConflictError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="RESOURCE_CONFLICT",
            message=message,
        )


class BadRequestError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="BAD_REQUEST",
            message=message,
        )