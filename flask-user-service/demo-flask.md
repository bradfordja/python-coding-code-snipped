# Flask User Microservice
Below is a reusable Flask User Microservice using:

* Flask application factory
* Flask Blueprints
* Flask-SQLAlchemy
* JWT authentication
* Role/permission authorization
* Service and repository layers
* User CRUD endpoints
* Centralized error handling
* SQLite for the demonstration
* Docker support

Flask’s application factory and Blueprint patterns are intended for modular applications, while Flask-JWT-Extended provides token creation and protected-route decorators.  

1. Project structure
```sh
flask-user-microservice/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── error_handlers.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── user_service.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py
│       ├── health_routes.py
│       └── user_routes.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_users.py
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── seed.py
```

Every package folder should contain an empty __init__.py.

2. Dependencies
```sh
# requirements.txt

Flask>=3.1,<4.0
Flask-SQLAlchemy>=3.1,<4.0
Flask-JWT-Extended>=4.7,<5.0
python-dotenv>=1.0,<2.0
marshmallow>=3.21,<5.0
gunicorn>=23.0,<24.0
pytest>=8.0,<9.0

Flask-SQLAlchemy manages SQLAlchemy integration and application-context lifecycle for Flask applications.  
```

3. Environment configuration
```sh
# .env.example

FLASK_ENV=development
SECRET_KEY=replace-with-a-random-secret
JWT_SECRET_KEY=replace-with-another-random-secret
DATABASE_URL=sqlite:///users.db
ACCESS_TOKEN_EXPIRES_MINUTES=30
```

Copy it:
```sh
cp .env.example .env
```

Generate secure secrets:
```sh
openssl rand -hex 32
```

```py
# app/core/config.py

import os
from datetime import timedelta
class BaseConfig:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-only",
    )
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "development-jwt-secret-only",
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///users.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(
            os.getenv(
                "ACCESS_TOKEN_EXPIRES_MINUTES",
                "30",
            )
        )
    )
    JSON_SORT_KEYS = False
class DevelopmentConfig(BaseConfig):
    DEBUG = True
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
CONFIG_BY_NAME = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
```

4. Shared extensions

Extensions are created separately and initialized inside the application factory. This avoids tightly coupling them to one Flask application instance.

```py
# app/extensions.py

from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
```

5. Application factory
```py
# app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask
from app.core.config import CONFIG_BY_NAME
from app.core.error_handlers import register_error_handlers
from app.extensions import db, jwt
def create_app(config_name: str | None = None) -> Flask:
    """
    Application factory.
    It creates and configures a new Flask application instance.
    This makes testing and running multiple environments easier.
    """
    load_dotenv()
    environment = config_name or os.getenv(
        "FLASK_ENV",
        "development",
    )
    app = Flask(__name__)
    config_class = CONFIG_BY_NAME.get(
        environment,
        CONFIG_BY_NAME["development"],
    )
    app.config.from_object(config_class)
    # Initialize Flask extensions.
    db.init_app(app)
    jwt.init_app(app)
    # Register routes.
    register_blueprints(app)
    # Register centralized exception handlers.
    register_error_handlers(app)
    # Register JWT-specific error handlers.
    register_jwt_handlers(jwt)
    return app
def register_blueprints(app: Flask) -> None:
    from app.routes.auth_routes import auth_blueprint
    from app.routes.health_routes import health_blueprint
    from app.routes.user_routes import user_blueprint
    app.register_blueprint(
        health_blueprint,
        url_prefix="/api/v1",
    )
    app.register_blueprint(
        auth_blueprint,
        url_prefix="/api/v1/auth",
    )
    app.register_blueprint(
        user_blueprint,
        url_prefix="/api/v1/users",
    )
def register_jwt_handlers(jwt_manager: JWTManager) -> None:
    """
    Return consistent JSON errors for JWT failures.
    """
    @jwt_manager.unauthorized_loader
    def missing_token(reason: str):
        return {
            "error": {
                "code": "MISSING_TOKEN",
                "message": reason,
                "details": None,
            }
        }, 401
    @jwt_manager.invalid_token_loader
    def invalid_token(reason: str):
        return {
            "error": {
                "code": "INVALID_TOKEN",
                "message": reason,
                "details": None,
            }
        }, 401
    @jwt_manager.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return {
            "error": {
                "code": "TOKEN_EXPIRED",
                "message": "The access token has expired",
                "details": None,
            }
        }, 401
    @jwt_manager.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        return {
            "error": {
                "code": "TOKEN_REVOKED",
                "message": "The access token has been revoked",
                "details": None,
            }
        }, 401
```

6. User model
```py
# app/models/user.py

from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
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
class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=Role.VIEWER.value,
    )
    disabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    def get_role(self) -> Role:
        return Role(self.role)
    def to_dict(self) -> dict:
        """
        Public representation.
        Never return password_hash to the client.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "disabled": self.disabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

```py
app/models/__init__.py

from app.models.user import User
__all__ = ["User"]
```

7. Custom exceptions
```py
# app/core/exceptions.py

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

8. Centralized error handling
```py
# app/core/error_handlers.py

import logging
from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import ApplicationError
from app.extensions import db
logger = logging.getLogger(__name__)
def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApplicationError)
    def handle_application_error(error: ApplicationError):
        return jsonify(
            {
                "error": {
                    "code": error.code,
                    "message": error.message,
                    "details": error.details,
                }
            }
        ), error.status_code
    @app.errorhandler(404)
    def handle_route_not_found(error):
        return jsonify(
            {
                "error": {
                    "code": "ROUTE_NOT_FOUND",
                    "message": "The requested endpoint does not exist",
                    "details": None,
                }
            }
        ), 404
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify(
            {
                "error": {
                    "code": "METHOD_NOT_ALLOWED",
                    "message": "The HTTP method is not allowed",
                    "details": None,
                }
            }
        ), 405
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error: SQLAlchemyError):
        db.session.rollback()
        logger.exception("Database error")
        return jsonify(
            {
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "A database operation failed",
                    "details": None,
                }
            }
        ), 500
    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        logger.exception("Unexpected application error")
        return jsonify(
            {
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                    "details": None,
                }
            }
        ), 500
```

9. Password security

Werkzeug is included with Flask and provides password-hashing helpers.
```py
# app/core/security.py

from functools import wraps
from typing import Callable
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
from app.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
)
from app.models.user import (
    Permission,
    ROLE_PERMISSIONS,
)
from app.repositories.user_repository import UserRepository
def hash_password(password: str) -> str:
    return generate_password_hash(
        password,
        method="scrypt",
    )
def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    return check_password_hash(
        password_hash,
        password,
    )
def permission_required(
    permission: Permission,
) -> Callable:
    """
    Protect a route and verify the user has a permission.
    Authentication:
        Is the token valid?
    Authorization:
        Does this authenticated user have access?
    """
    def decorator(route_function: Callable) -> Callable:
        @wraps(route_function)
        @jwt_required()
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity is None:
                raise AuthenticationError(
                    "The token does not contain a user identity"
                )
            try:
                user_id = int(identity)
            except (TypeError, ValueError) as error:
                raise AuthenticationError(
                    "The token contains an invalid user identity"
                ) from error
            user = UserRepository.find_by_id(user_id)
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
            permissions = ROLE_PERMISSIONS.get(
                user.get_role(),
                set(),
            )
            if permission not in permissions:
                raise AuthorizationError(
                    f"Permission '{permission.value}' is required"
                )
            # Pass the authenticated user into the route.
            return route_function(
                *args,
                current_user=user,
                **kwargs,
            )
        return wrapper
    return decorator
```

The database is checked on every protected request. Therefore, role changes and disabled accounts take effect without waiting for the JWT to expire.

10. Validation schemas
```py
# app/schemas/user_schema.py

from marshmallow import (
    Schema,
    ValidationError as MarshmallowValidationError,
    fields,
    validate,
    validates_schema,
)
from app.models.user import Role
class UserCreateSchema(Schema):
    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(r"^[a-zA-Z0-9_.-]+$"),
        ],
    )
    email = fields.Email(required=True)
    full_name = fields.String(
        required=True,
        validate=validate.Length(min=2, max=100),
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )
    role = fields.String(
        load_default=Role.VIEWER.value,
        validate=validate.OneOf(
            [role.value for role in Role]
        ),
    )
class UserUpdateSchema(Schema):
    email = fields.Email(required=False)
    full_name = fields.String(
        required=False,
        validate=validate.Length(min=2, max=100),
    )
    password = fields.String(
        required=False,
        load_only=True,
        validate=validate.Length(min=8, max=128),
    )
    role = fields.String(
        required=False,
        validate=validate.OneOf(
            [role.value for role in Role]
        ),
    )
    disabled = fields.Boolean(required=False)
    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise MarshmallowValidationError(
                "At least one field must be supplied"
            )
class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
```
11. Repository layer

Repositories contain database operations only.
```py
# app/repositories/user_repository.py

from sqlalchemy import select
from app.extensions import db
from app.models.user import User
class UserRepository:
    @staticmethod
    def find_all(
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[User], int]:
        statement = (
            select(User)
            .order_by(User.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        users = list(
            db.session.scalars(statement).all()
        )
        total_statement = select(
            db.func.count(User.id)
        )
        total = db.session.scalar(total_statement) or 0
        return users, total
    @staticmethod
    def find_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)
    @staticmethod
    def find_by_username(username: str) -> User | None:
        statement = select(User).where(
            db.func.lower(User.username)
            == username.lower()
        )
        return db.session.scalar(statement)
    @staticmethod
    def find_by_email(email: str) -> User | None:
        statement = select(User).where(
            db.func.lower(User.email)
            == email.lower()
        )
        return db.session.scalar(statement)
    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        return user
    @staticmethod
    def update(user: User) -> User:
        db.session.commit()
        db.session.refresh(user)
        return user
    @staticmethod
    def delete(user: User) -> None:
        db.session.delete(user)
        db.session.commit()
```

12. Authentication service
```py
# app/services/auth_service.py

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
```

13. User service
```py
# app/services/user_service.py

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
```

14. Authentication routes
```py
app/routes/auth_routes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from marshmallow import ValidationError as MarshmallowValidationError
from app.core.exceptions import (
    AuthenticationError,
    ValidationError,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import LoginSchema
from app.services.auth_service import AuthService
auth_blueprint = Blueprint(
    "authentication",
    __name__,
)
login_schema = LoginSchema()
@auth_blueprint.post("/login")
def login():
    try:
        data = login_schema.load(
            request.get_json(silent=True) or {}
        )
    except MarshmallowValidationError as error:
        raise ValidationError(error.messages) from error
    result = AuthService.login(
        username=data["username"],
        password=data["password"],
    )
    return jsonify(result), 200
@auth_blueprint.get("/me")
@jwt_required()
def get_current_profile():
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError) as error:
        raise AuthenticationError(
            "Invalid JWT user identity"
        ) from error
    user = UserRepository.find_by_id(user_id)
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
    return jsonify(user.to_dict()), 200
```

15. User CRUD routes
```py
# app/routes/user_routes.py

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError as MarshmallowValidationError
from app.core.exceptions import ValidationError
from app.core.security import permission_required
from app.models.user import Permission, User
from app.schemas.user_schema import (
    UserCreateSchema,
    UserUpdateSchema,
)
from app.services.user_service import UserService
user_blueprint = Blueprint(
    "users",
    __name__,
)
create_schema = UserCreateSchema()
update_schema = UserUpdateSchema()
@user_blueprint.get("")
@permission_required(Permission.USER_READ)
def get_users(current_user: User):
    page = request.args.get(
        "page",
        default=1,
        type=int,
    )
    page_size = request.args.get(
        "page_size",
        default=20,
        type=int,
    )
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)
    result = UserService.get_users(
        page=page,
        page_size=page_size,
    )
    return jsonify(result), 200
@user_blueprint.get("/<int:user_id>")
@permission_required(Permission.USER_READ)
def get_user(
    user_id: int,
    current_user: User,
):
    user = UserService.get_user(user_id)
    return jsonify(user.to_dict()), 200
@user_blueprint.post("")
@permission_required(Permission.USER_CREATE)
def create_user(current_user: User):
    try:
        data = create_schema.load(
            request.get_json(silent=True) or {}
        )
    except MarshmallowValidationError as error:
        raise ValidationError(error.messages) from error
    user = UserService.create_user(data)
    return jsonify(user.to_dict()), 201
@user_blueprint.patch("/<int:user_id>")
@permission_required(Permission.USER_UPDATE)
def update_user(
    user_id: int,
    current_user: User,
):
    try:
        data = update_schema.load(
            request.get_json(silent=True) or {}
        )
    except MarshmallowValidationError as error:
        raise ValidationError(error.messages) from error
    user = UserService.update_user(
        user_id=user_id,
        data=data,
    )
    return jsonify(user.to_dict()), 200
@user_blueprint.delete("/<int:user_id>")
@permission_required(Permission.USER_DELETE)
def delete_user(
    user_id: int,
    current_user: User,
):
    UserService.delete_user(
        user_id=user_id,
        current_user=current_user,
    )
    return "", 204
```

16. Health endpoint
```py
# app/routes/health_routes.py

from flask import Blueprint, jsonify
from sqlalchemy import text
from app.extensions import db
health_blueprint = Blueprint(
    "health",
    __name__,
)
@health_blueprint.get("/health")
def health():
    return jsonify(
        {
            "status": "UP",
            "service": "user-service",
        }
    ), 200
@health_blueprint.get("/health/ready")
def readiness():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify(
            {
                "status": "READY",
                "database": "UP",
            }
        ), 200
    except Exception:
        return jsonify(
            {
                "status": "NOT_READY",
                "database": "DOWN",
            }
        ), 503
```

17. Application entry point
```py
# run.py

from app import create_app
app = create_app()
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=app.config["DEBUG"],
    )
```

18. Seed script
```py
# seed.py

from app import create_app
from app.core.security import hash_password
from app.extensions import db
from app.models.user import Role, User
from app.repositories.user_repository import UserRepository
app = create_app()
def create_seed_users() -> None:
    with app.app_context():
        db.create_all()
        if UserRepository.find_by_username("admin") is None:
            admin = User(
                username="admin",
                email="admin@example.com",
                full_name="System Administrator",
                password_hash=hash_password("Admin123!"),
                role=Role.ADMIN.value,
                disabled=False,
            )
            db.session.add(admin)
        if UserRepository.find_by_username("viewer") is None:
            viewer = User(
                username="viewer",
                email="viewer@example.com",
                full_name="Read Only User",
                password_hash=hash_password("Viewer123!"),
                role=Role.VIEWER.value,
                disabled=False,
            )
            db.session.add(viewer)
        db.session.commit()
        print("Database and demonstration users created.")
if __name__ == "__main__":
    create_seed_users()
```
19. Run locally

Create a virtual environment:

python -m venv .venv

Activate on macOS or Linux:

source .venv/bin/activate

Activate on Windows PowerShell:

.venv\Scripts\Activate.ps1

Install and seed:

pip install -r requirements.txt
python seed.py
python run.py

The service runs at:

http://localhost:5000

20. Test the API

Login

curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "Admin123!"
  }'

Save the returned token:

TOKEN="paste-token-here"

Read users

curl http://localhost:5000/api/v1/users \
  -H "Authorization: Bearer $TOKEN"

Create a user

curl -X POST http://localhost:5000/api/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jsmith",
    "email": "jsmith@example.com",
    "full_name": "John Smith",
    "password": "Password123!",
    "role": "viewer"
  }'

Update a user

curl -X PATCH http://localhost:5000/api/v1/users/2 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Viewer",
    "disabled": false
  }'

Delete a user

curl -X DELETE http://localhost:5000/api/v1/users/2 \
  -H "Authorization: Bearer $TOKEN"

21. Docker configuration

Dockerfile
```yml
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    -r requirements.txt
COPY . .
RUN python seed.py
EXPOSE 5000
CMD [
  "gunicorn",
  "--bind",
  "0.0.0.0:5000",
  "--workers",
  "2",
  "--threads",
  "4",
  "run:app"
]
```

docker-compose.yml
```yml
services:
  user-service:
    build:
      context: .
    container_name: user-service
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
      DATABASE_URL: sqlite:////data/users.db
      ACCESS_TOKEN_EXPIRES_MINUTES: 30
    volumes:
      - user-data:/data
    restart: unless-stopped
volumes:
  user-data:
```
Run it:

docker compose up --build

22. Basic test configuration
```py
# tests/conftest.py

import pytest
from app import create_app
from app.extensions import db
@pytest.fixture
def app():
    application = create_app("testing")
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()
@pytest.fixture
def client(app):
    return app.test_client()

tests/test_users.py

from app.core.security import hash_password
from app.extensions import db
from app.models.user import Role, User
def create_admin(app):
    with app.app_context():
        admin = User(
            username="admin",
            email="admin@example.com",
            full_name="Administrator",
            password_hash=hash_password("Admin123!"),
            role=Role.ADMIN.value,
            disabled=False,
        )
        db.session.add(admin)
        db.session.commit()
def login_admin(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": "admin",
            "password": "Admin123!",
        },
    )
    return response.get_json()["access_token"]
def test_admin_can_create_user(app, client):
    create_admin(app)
    token = login_admin(client)
    response = client.post(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {token}",
        },
        json={
            "username": "jsmith",
            "email": "jsmith@example.com",
            "full_name": "John Smith",
            "password": "Password123!",
            "role": "viewer",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["username"] == "jsmith"
def test_users_endpoint_requires_token(client):
    response = client.get("/api/v1/users")
    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == (
        "MISSING_TOKEN"
    )
```
Run tests:

pytest -v

Microservice separation

This project represents one independently deployable service:
```sh
API Gateway
    |
    +-- Identity Service
    |      Login, refresh tokens, token revocation
    |
    +-- User Service
    |      User profiles and user CRUD
    |
    +-- Product Service
    |      Products and inventory
    |
    +-- Order Service
           Orders and payments
```
For a larger architecture, authentication can be moved into a dedicated identity service. Other services should validate tokens using a public key or identity-provider introspection rather than sharing user-service repository code. Each service should own its own database and communicate through REST, gRPC, or Kafka rather than importing another service’s internal classes.