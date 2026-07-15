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