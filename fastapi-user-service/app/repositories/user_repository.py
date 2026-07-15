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