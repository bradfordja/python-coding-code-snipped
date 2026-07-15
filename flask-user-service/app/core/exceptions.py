from typing import Any


class ApplicationError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        code: str = "APPLICATION_ERROR",
        details: Any | None = None,
    ):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details


class AuthenticationError(ApplicationError):
    def __init__(
        self,
        message: str = "Authentication failed",
        code: str = "AUTHENTICATION_FAILED",
    ):
        super().__init__(
            message=message,
            status_code=401,
            code=code,
        )


class AuthorizationError(ApplicationError):
    def __init__(
        self,
        message: str = "Access denied",
    ):
        super().__init__(
            message=message,
            status_code=403,
            code="ACCESS_DENIED",
        )


class NotFoundError(ApplicationError):
    def __init__(
        self,
        resource: str,
        resource_id: object,
    ):
        super().__init__(
            message=f"{resource} was not found",
            status_code=404,
            code="RESOURCE_NOT_FOUND",
            details={
                "resource": resource,
                "id": resource_id,
            },
        )


class ConflictError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=409,
            code="RESOURCE_CONFLICT",
        )


class ValidationError(ApplicationError):
    def __init__(self, details: dict | list):
        super().__init__(
            message="The request contains invalid data",
            status_code=422,
            code="VALIDATION_ERROR",
            details=details,
        )