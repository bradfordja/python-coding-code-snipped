# FastAPI

Below is a complete, runnable FastAPI example that provides:
```sh
* JWT authentication
* Password hashing
* Role-based authorization
* User CRUD operations
* Admin and viewer roles
* Validation and centralized error handling
* Swagger/OpenAPI login support
* In-memory data storage for simplicity
```

FastAPI supports OAuth2 bearer-token dependencies and OAuth2 scopes; the example below uses bearer authentication with a straightforward role/permission dependency.  

## Project structure
```sh
fastapi-user-security/
├── main.py
├── requirements.txt
└── .env
```

## Packages 
```sh
requirements.txt
fastapi
uvicorn[standard]
python-multipart
PyJWT
pwdlib[argon2]
pydantic[email]
python-dotenv
python-multipart is required because the OAuth2 login endpoint receives form data.
```

## Enviroment
.env

### Generate a strong secret instead of using a simple password:
```sh
JWT_SECRET_KEY=replace-this-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## One way to generate a secret:
```sh
openssl rand -hex 32
```

# main.py
```sh
# main.py
import os
from datetime import datetime, timedelta, timezone
from enum import Enum
from threading import Lock
from typing import Annotated, Any, Callable

import jwt
from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Security,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from jwt import ExpiredSignatureError, InvalidTokenError
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pwdlib import PasswordHash


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

load_dotenv()

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-only-secret-change-this"
)

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Secure User CRUD API",
    version="1.0.0",
    description=(
        "FastAPI example using JWT authentication and "
        "role-based authorization."
    ),
)


# ---------------------------------------------------------
# Security configuration
# ---------------------------------------------------------

# Recommended password hashing configuration from pwdlib.
password_hash = PasswordHash.recommended()

# Reads: Authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=False)


# ---------------------------------------------------------
# Roles and permissions
# ---------------------------------------------------------

class Role(str, Enum):
    ADMIN = "admin"
    VIEWER = "viewer"


class Permission(str, Enum):
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"


# Permissions assigned to each role.
ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.ADMIN: {
        Permission.USER_CREATE,
        Permission.USER_READ,
        Permission.USER_UPDATE,
        Permission.USER_DELETE,
    },
    Role.VIEWER: {
        Permission.USER_READ,
    },
}


# ---------------------------------------------------------
# Pydantic request and response models
# ---------------------------------------------------------

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_.-]+$",
    )
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)
    role: Role = Role.VIEWER


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
    )
    role: Role | None = None
    disabled: bool | None = None


class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    hashed_password: str
    role: Role
    disabled: bool = False


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    full_name: str
    role: Role
    disabled: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: str
    role: Role
    exp: int


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


# ---------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------

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
        message: str = "You do not have permission to perform this action",
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="ACCESS_DENIED",
            message=message,
        )


class ResourceNotFoundError(ApplicationError):
    def __init__(self, resource: str, resource_id: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="RESOURCE_NOT_FOUND",
            message=f"{resource} was not found",
            details={"resource": resource, "id": resource_id},
        )


class ConflictError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code="RESOURCE_CONFLICT",
            message=message,
        )


# ---------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------

@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    headers = None

    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        headers = {"WWW-Authenticate": "Bearer"}

    return JSONResponse(
        status_code=exc.status_code,
        headers=headers,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = []

    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(item) for item in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The request contains invalid data",
                "details": errors,
            }
        },
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    # Log the real exception in a production application.
    print(f"Unexpected error: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred",
                "details": None,
            }
        },
    )


# ---------------------------------------------------------
# In-memory user repository
# Replace this section with SQLAlchemy in production.
# ---------------------------------------------------------

users_by_id: dict[int, UserInDB] = {}
user_ids_by_username: dict[str, int] = {}
repository_lock = Lock()
next_user_id = 1


def seed_users() -> None:
    """Create demonstration users when the application starts."""

    global next_user_id

    initial_users = [
        UserInDB(
            id=1,
            username="admin",
            email="admin@example.com",
            full_name="System Administrator",
            hashed_password=password_hash.hash("Admin123!"),
            role=Role.ADMIN,
            disabled=False,
        ),
        UserInDB(
            id=2,
            username="viewer",
            email="viewer@example.com",
            full_name="Read Only User",
            hashed_password=password_hash.hash("Viewer123!"),
            role=Role.VIEWER,
            disabled=False,
        ),
    ]

    for user in initial_users:
        users_by_id[user.id] = user
        user_ids_by_username[user.username.lower()] = user.id

    next_user_id = 3


seed_users()


def find_user_by_username(username: str) -> UserInDB | None:
    user_id = user_ids_by_username.get(username.lower())

    if user_id is None:
        return None

    return users_by_id.get(user_id)


def find_user_by_id(user_id: int) -> UserInDB | None:
    return users_by_id.get(user_id)


# ---------------------------------------------------------
# Authentication functions
# ---------------------------------------------------------

def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return password_hash.verify(
        plain_password,
        hashed_password,
    )


def authenticate_user(
    username: str,
    password: str,
) -> UserInDB | None:
    user = find_user_by_username(username)

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(user: UserInDB) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        # Subject identifies the authenticated user.
        "sub": user.username,

        # Role is included for informational purposes.
        # Current permissions are still checked against the stored user.
        "role": user.role.value,

        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={
                "require": ["sub", "role", "exp"],
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


# ---------------------------------------------------------
# Authentication dependency
# ---------------------------------------------------------

def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
) -> UserInDB:
    if credentials is None:
        raise AuthenticationError(
            message="A bearer token is required",
            code="MISSING_TOKEN",
        )

    if credentials.scheme.lower() != "bearer":
        raise AuthenticationError(
            message="The authorization scheme must be Bearer",
            code="INVALID_AUTHORIZATION_SCHEME",
        )

    token_payload = decode_access_token(credentials.credentials)

    user = find_user_by_username(token_payload.sub)

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

    return user


CurrentUser = Annotated[UserInDB, Depends(get_current_user)]


# ---------------------------------------------------------
# Authorization dependency factory
# ---------------------------------------------------------

def require_permission(
    permission: Permission,
) -> Callable[[UserInDB], UserInDB]:
    """
    Creates a FastAPI dependency that checks whether the current
    user's role contains the required permission.
    """

    def permission_checker(
        current_user: CurrentUser,
    ) -> UserInDB:
        user_permissions = ROLE_PERMISSIONS.get(
            current_user.role,
            set(),
        )

        if permission not in user_permissions:
            raise AuthorizationError(
                message=(
                    f"Permission '{permission.value}' is required"
                )
            )

        return current_user

    return permission_checker


CanCreateUsers = Annotated[
    UserInDB,
    Security(require_permission(Permission.USER_CREATE)),
]

CanReadUsers = Annotated[
    UserInDB,
    Security(require_permission(Permission.USER_READ)),
]

CanUpdateUsers = Annotated[
    UserInDB,
    Security(require_permission(Permission.USER_UPDATE)),
]

CanDeleteUsers = Annotated[
    UserInDB,
    Security(require_permission(Permission.USER_DELETE)),
]


# ---------------------------------------------------------
# Public endpoints
# ---------------------------------------------------------

@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Secure User CRUD API",
        "documentation": "/docs",
    }


@app.post(
    "/auth/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
) -> TokenResponse:
    """
    Authenticate with a username and password.

    OAuth2PasswordRequestForm expects form fields named:
    - username
    - password
    """

    user = authenticate_user(
        form_data.username,
        form_data.password,
    )

    if user is None:
        raise AuthenticationError(
            message="Incorrect username or password",
            code="INVALID_CREDENTIALS",
        )

    if user.disabled:
        raise AuthorizationError(
            message="This user account has been disabled"
        )

    access_token = create_access_token(user)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ---------------------------------------------------------
# Current user endpoint
# ---------------------------------------------------------

@app.get(
    "/auth/me",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse},
    },
)
def get_my_profile(
    current_user: CurrentUser,
) -> UserResponse:
    return UserResponse.model_validate(current_user)


# ---------------------------------------------------------
# User CRUD endpoints
# ---------------------------------------------------------

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
def create_user(
    request: UserCreate,
    current_user: CanCreateUsers,
) -> UserResponse:
    """
    Create a user.

    Required permission: user:create
    Admin users have this permission.
    """

    global next_user_id

    normalized_username = request.username.lower()

    with repository_lock:
        if normalized_username in user_ids_by_username:
            raise ConflictError(
                f"Username '{request.username}' already exists"
            )

        if any(
            existing.email.lower() == request.email.lower()
            for existing in users_by_id.values()
        ):
            raise ConflictError(
                f"Email '{request.email}' already exists"
            )

        user = UserInDB(
            id=next_user_id,
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            hashed_password=password_hash.hash(request.password),
            role=request.role,
            disabled=False,
        )

        users_by_id[user.id] = user
        user_ids_by_username[normalized_username] = user.id
        next_user_id += 1

    return UserResponse.model_validate(user)


@app.get(
    "/users",
    response_model=list[UserResponse],
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
)
def get_users(
    current_user: CanReadUsers,
    skip: int = 0,
    limit: int = 100,
) -> list[UserResponse]:
    """
    Return the user list.

    Both admin and viewer roles have user:read permission.
    """

    if skip < 0:
        raise ApplicationError(
            status_code=400,
            code="INVALID_PAGINATION",
            message="skip cannot be negative",
        )

    if limit < 1 or limit > 100:
        raise ApplicationError(
            status_code=400,
            code="INVALID_PAGINATION",
            message="limit must be between 1 and 100",
        )

    users = sorted(
        users_by_id.values(),
        key=lambda item: item.id,
    )

    selected_users = users[skip: skip + limit]

    return [
        UserResponse.model_validate(user)
        for user in selected_users
    ]


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
def get_user(
    user_id: int,
    current_user: CanReadUsers,
) -> UserResponse:
    user = find_user_by_id(user_id)

    if user is None:
        raise ResourceNotFoundError("User", user_id)

    return UserResponse.model_validate(user)


@app.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)
def update_user(
    user_id: int,
    request: UserUpdate,
    current_user: CanUpdateUsers,
) -> UserResponse:
    """
    Partially update a user.

    Required permission: user:update
    """

    existing_user = find_user_by_id(user_id)

    if existing_user is None:
        raise ResourceNotFoundError("User", user_id)

    updates = request.model_dump(exclude_unset=True)

    if "email" in updates:
        requested_email = str(updates["email"]).lower()

        email_in_use = any(
            user.id != user_id
            and user.email.lower() == requested_email
            for user in users_by_id.values()
        )

        if email_in_use:
            raise ConflictError(
                f"Email '{updates['email']}' already exists"
            )

    # Hash the new password instead of storing plain text.
    if "password" in updates:
        updates["hashed_password"] = password_hash.hash(
            updates.pop("password")
        )

    updated_user = existing_user.model_copy(update=updates)

    with repository_lock:
        users_by_id[user_id] = updated_user

    return UserResponse.model_validate(updated_user)


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
def delete_user(
    user_id: int,
    current_user: CanDeleteUsers,
) -> None:
    """
    Delete a user.

    Required permission: user:delete
    """

    user = find_user_by_id(user_id)

    if user is None:
        raise ResourceNotFoundError("User", user_id)

    # Prevent administrators from deleting their own active account.
    if user.id == current_user.id:
        raise ConflictError(
            "You cannot delete your own authenticated account"
        )

    with repository_lock:
        users_by_id.pop(user_id, None)
        user_ids_by_username.pop(user.username.lower(), None)

    return None
5. Run the application
Create and activate a virtual environment:
python -m venv .venv
macOS or Linux:
source .venv/bin/activate
Windows PowerShell:
.venv\Scripts\Activate.ps1
Install dependencies:
pip install -r requirements.txt
Start FastAPI:
uvicorn main:app --reload
Open Swagger UI:
http://127.0.0.1:8000/docs
6. Test accounts
Username	Password	Role	Access
admin	Admin123!	Admin	Full CRUD
viewer	Viewer123!	Viewer	Read only
These credentials are only demonstration values.
7. Test using
curl
Log in as administrator
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=Admin123!"
Example response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
Save the token:
TOKEN="paste-access-token-here"
Get the current user
curl "http://127.0.0.1:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
Get all users
curl "http://127.0.0.1:8000/users" \
  -H "Authorization: Bearer $TOKEN"
Create a user
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john.smith",
    "email": "john.smith@example.com",
    "full_name": "John Smith",
    "password": "Password123!",
    "role": "viewer"
  }'
Update a user
curl -X PATCH "http://127.0.0.1:8000/users/2" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Viewer",
    "disabled": false
  }'
Delete a user
curl -X DELETE "http://127.0.0.1:8000/users/2" \
  -H "Authorization: Bearer $TOKEN"
8. Authorization behavior
A viewer can execute:
GET /users
GET /users/{user_id}
GET /auth/me
A viewer receives HTTP 403 Forbidden for:
POST /users
PATCH /users/{user_id}
DELETE /users/{user_id}
Example error:
{
  "error": {
    "code": "ACCESS_DENIED",
    "message": "Permission 'user:create' is required",
    "details": null
  }
}
An invalid or expired token returns HTTP 401 Unauthorized:
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "The access token has expired",
    "details": null
  }
}

PyJWT validates token signatures during decoding, supports explicit algorithm selection, and verifies expiration claims.  
For production, replace the in-memory dictionaries with PostgreSQL and SQLAlchemy, keep the JWT secret in a secrets manager, use HTTPS, add refresh-token rotation, audit logging, rate limiting, and database-level uniqueness constraints.
