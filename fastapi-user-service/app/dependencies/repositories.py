from app.repositories.user_repository import UserRepository

user_repository = UserRepository()

def get_user_repository() -> UserRepository:
    return user_repository