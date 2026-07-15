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