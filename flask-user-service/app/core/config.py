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