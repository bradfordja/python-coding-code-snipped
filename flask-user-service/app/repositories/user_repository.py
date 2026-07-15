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