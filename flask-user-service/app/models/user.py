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