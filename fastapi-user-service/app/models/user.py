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