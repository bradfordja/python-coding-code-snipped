# independent microservices
Yes. A layered structure makes the application easier to extend into additional APIs or independent microservices.

The main flow becomes:

```sh
Router → Service → Repository → Database
             ↓
      Security / Exceptions
```

Project structure

```sh
fastapi-user-service/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── exception_handlers.py
│   │   └── security.py
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── repositories.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── error.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── base.py
│   │   └── user_repository.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── user_service.py
│   └── routers/
│       ├── auth_router.py
│       └── user_router.py
├── tests/
│   └── test_users.py
├── .env
└── requirements.txt
```

Add empty __init__.py files to each Python package directory.

⸻

## Dependencies

requirements.txt
```sh
fastapi
uvicorn[standard]
python-multipart
PyJWT
pwdlib[argon2]
pydantic[email]
pydantic-settings
pytest
httpx
```
⸻

2. Environment configuration

.env

```sh
APP_NAME=User Management Service
APP_VERSION=1.0.0
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

```py
## app/core/config.py

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    app_name: str = "User Management Service"
    app_version: str = "1.0.0"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
@lru_cache
def get_settings() -> Settings:
    """
    Create the settings object once and reuse it.
    FastAPI dependencies can also override this function during tests.
    """
    return Settings()
settings = get_settings()
```
⸻

## Domain model

The model represents data stored internally. In production, this would normally be a SQLAlchemy model.

```py
## app/models/user.py

from enum import Enum
from pydantic import BaseModel, EmailStr
class Role(str, Enum):
    ADMIN = "admin"
    VIEWER = "viewer"
class Permission(str, Enum):
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
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
class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    hashed_password: str
    role: Role
    disabled: bool = False
```

⸻

## API schemas

Schemas define what clients can send and receive.
```py
## app/schemas/user.py

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.user import Role
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
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    full_name: str
    role: Role
    disabled: bool
```

```py
## app/schemas/auth.py

from pydantic import BaseModel
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
class TokenPayload(BaseModel):
    sub: str
    exp: int
```

```py
## app/schemas/error.py

from typing import Any
from pydantic import BaseModel
class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any | None = None
class ErrorResponse(BaseModel):
    error: ErrorDetail
```
⸻

## Shared exceptions
```py
## app/core/exceptions.py

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
```
⸻

## Global exception handlers
```py
## app/core/exception_handlers.py

import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.exceptions import ApplicationError
logger = logging.getLogger(__name__)
def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application-wide exception handlers.
    """
    @app.exception_handler(ApplicationError)
    async def handle_application_error(
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
    async def handle_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        validation_details = [
            {
                "field": ".".join(
                    str(location) for location in error["loc"]
                ),
                "message": error["msg"],
                "type": error["type"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "The request contains invalid data",
                    "details": validation_details,
                }
            },
        )
    @app.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception(
            "Unexpected error while processing %s",
            request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": None,
                }
            },
        )
```
⸻

## Security utility

This component handles only passwords and JWT tokens.
```py
## app/core/security.py

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
```

⸻

## Repository layer

The repository handles data access only. It does not contain authentication or business rules.

```py
## app/repositories/base.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
EntityType = TypeVar("EntityType")
class BaseRepository(ABC, Generic[EntityType]):
    @abstractmethod
    def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[EntityType]:
        raise NotImplementedError
    @abstractmethod
    def find_by_id(self, entity_id: int) -> EntityType | None:
        raise NotImplementedError
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        raise NotImplementedError
```

```py
## app/repositories/user_repository.py

from threading import Lock
from app.core.security import hash_password
from app.models.user import Role, User
from app.repositories.base import BaseRepository
class UserRepository(BaseRepository[User]):
    """
    In-memory repository.
    Replace this implementation with SQLAlchemy, MongoDB,
    DynamoDB or another persistence technology later.
    """
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._username_index: dict[str, int] = {}
        self._next_id = 1
        self._lock = Lock()
        self._seed_users()
    def _seed_users(self) -> None:
        self.create(
            username="admin",
            email="admin@example.com",
            full_name="System Administrator",
            hashed_password=hash_password("Admin123!"),
            role=Role.ADMIN,
        )
        self.create(
            username="viewer",
            email="viewer@example.com",
            full_name="Read Only User",
            hashed_password=hash_password("Viewer123!"),
            role=Role.VIEWER,
        )
    def find_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        users = sorted(
            self._users.values(),
            key=lambda user: user.id,
        )
        return users[skip:skip + limit]
    def find_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)
    def find_by_username(self, username: str) -> User | None:
        user_id = self._username_index.get(username.lower())
        if user_id is None:
            return None
        return self._users.get(user_id)
    def find_by_email(self, email: str) -> User | None:
        normalized_email = email.lower()
        return next(
            (
                user
                for user in self._users.values()
                if user.email.lower() == normalized_email
            ),
            None,
        )
    def create(
        self,
        username: str,
        email: str,
        full_name: str,
        hashed_password: str,
        role: Role,
    ) -> User:
        with self._lock:
            user = User(
                id=self._next_id,
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=hashed_password,
                role=role,
                disabled=False,
            )
            self._users[user.id] = user
            self._username_index[username.lower()] = user.id
            self._next_id += 1
            return user
    def update(
        self,
        user_id: int,
        updates: dict,
    ) -> User | None:
        with self._lock:
            existing_user = self._users.get(user_id)
            if existing_user is None:
                return None
            updated_user = existing_user.model_copy(
                update=updates
            )
            self._users[user_id] = updated_user
            return updated_user
    def delete(self, user_id: int) -> bool:
        with self._lock:
            user = self._users.pop(user_id, None)
            if user is None:
                return False
            self._username_index.pop(
                user.username.lower(),
                None,
            )
            return True
```
⸻

## Repository dependency

This creates one repository instance that can be injected wherever needed.
```py
## app/dependencies/repositories.py

from app.repositories.user_repository import UserRepository
user_repository = UserRepository()
def get_user_repository() -> UserRepository:
    return user_repository
```
Later, this dependency can return a database-backed repository instead.

⸻

## Authentication service
```py
## app/services/auth_service.py

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
```
⸻

## User service

The service contains business rules.
```py
## app/services/user_service.py

from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
)
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    def get_all_users(
        self,
        skip: int,
        limit: int,
    ) -> list[User]:
        if skip < 0:
            raise BadRequestError(
                "skip cannot be negative"
            )
        if limit < 1 or limit > 100:
            raise BadRequestError(
                "limit must be between 1 and 100"
            )
        return self.user_repository.find_all(
            skip=skip,
            limit=limit,
        )
    def get_user(self, user_id: int) -> User:
        user = self.user_repository.find_by_id(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user
    def create_user(self, request: UserCreate) -> User:
        existing_username = (
            self.user_repository.find_by_username(
                request.username
            )
        )
        if existing_username:
            raise ConflictError(
                f"Username '{request.username}' already exists"
            )
        existing_email = self.user_repository.find_by_email(
            str(request.email)
        )
        if existing_email:
            raise ConflictError(
                f"Email '{request.email}' already exists"
            )
        return self.user_repository.create(
            username=request.username,
            email=str(request.email),
            full_name=request.full_name,
            hashed_password=hash_password(request.password),
            role=request.role,
        )
    def update_user(
        self,
        user_id: int,
        request: UserUpdate,
    ) -> User:
        self.get_user(user_id)
        updates = request.model_dump(exclude_unset=True)
        if "email" in updates:
            existing_email = self.user_repository.find_by_email(
                str(updates["email"])
            )
            if (
                existing_email is not None
                and existing_email.id != user_id
            ):
                raise ConflictError(
                    f"Email '{updates['email']}' already exists"
                )
        if "password" in updates:
            updates["hashed_password"] = hash_password(
                updates.pop("password")
            )
        updated_user = self.user_repository.update(
            user_id,
            updates,
        )
        if updated_user is None:
            raise NotFoundError("User", user_id)
        return updated_user
    def delete_user(
        self,
        user_id: int,
        authenticated_user: User,
    ) -> None:
        user = self.get_user(user_id)
        if user.id == authenticated_user.id:
            raise ConflictError(
                "You cannot delete your own account"
            )
        deleted = self.user_repository.delete(user_id)
        if not deleted:
            raise NotFoundError("User", user_id)
```
⸻

## Authentication and authorization dependencies

```py
## app/dependencies/auth.py

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
```
⸻

## Authentication router

```py
## app/routers/auth_router.py

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import CurrentUser
from app.dependencies.repositories import get_user_repository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
) -> TokenResponse:
    auth_service = AuthService(user_repository)
    return auth_service.login(
        username=form_data.username,
        password=form_data.password,
    )
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_profile(
    current_user: CurrentUser,
) -> UserResponse:
    return UserResponse.model_validate(current_user)
```
⸻

14. User CRUD router

The router handles HTTP concerns only.

app/routers/user_router.py
```py
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
```
⸻

15. Main application

app/main.py
```py
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.core.config import settings
from app.core.exception_handlers import (
    register_exception_handlers,
)
from app.routers import auth_router, user_router
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s %(levelname)s "
        "%(name)s %(message)s"
    ),
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic:
    # - connect to database
    # - initialize Kafka producer
    # - initialize Redis client
    print(f"Starting {settings.app_name}")
    yield
    # Shutdown logic:
    # - close database connection
    # - close Kafka producer
    # - close Redis client
    print(f"Stopping {settings.app_name}")
def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )
    register_exception_handlers(app)
    app.include_router(
        auth_router.router,
        prefix="/api/v1",
    )
    app.include_router(
        user_router.router,
        prefix="/api/v1",
    )
    @app.get("/health", tags=["Health"])
    def health_check() -> dict[str, str]:
        return {
            "status": "UP",
            "service": settings.app_name,
        }
    return app
app = create_application()
```

Run it with:
```sh
uvicorn app.main:app --reload
```

Swagger:
```sh
http://127.0.0.1:8000/docs
```
⸻

Adding another API module

For example, to add a product API, use the same pattern:
```sh
models/product.py
schemas/product.py
repositories/product_repository.py
services/product_service.py
routers/product_router.py
```

Example product router
```py
from typing import Annotated
from fastapi import APIRouter, Depends
from app.dependencies.auth import CurrentUser
router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
@router.get("")
def get_products(
    current_user: CurrentUser,
) -> list[dict]:
    return [
        {
            "id": 1,
            "name": "Laptop",
            "price": 1200.00,
        }
    ]
```

Register it in main.py:
```sh
from app.routers import product_router
app.include_router(
    product_router.router,
    prefix="/api/v1",
)
```

The resulting endpoint is:
```sh
GET /api/v1/products
```
⸻

Separating into microservices

The modular application can later become:
```sh
services/
├── identity-service/
│   ├── authentication
│   ├── JWT issuance
│   └── roles and permissions
│
├── user-service/
│   ├── user profiles
│   └── user CRUD
│
├── product-service/
│   ├── products
│   └── inventory
│
└── order-service/
    ├── orders
    └── payments
```

A common request flow would be:
```sh
Client
  ↓
API Gateway
  ↓
Product Service
  ↓
Validate JWT issued by Identity Service
  ↓
Check roles or permissions
  ↓
Execute product operation
```

Each microservice should have its own:
```sh
main.py
routers/
services/
repositories/
schemas/
models/
core/
tests/
Dockerfile
requirements.txt
```

Shared authentication code can be packaged as an internal library:
```sh
shared-security/
├── token_decoder.py
├── authorization.py
├── exceptions.py
└── pyproject.toml
```

However, each microservice should own its business logic and database. Avoid importing repositories or service classes directly from another microservice. Communication between services should occur through REST, gRPC, Kafka, or another explicit API contract.