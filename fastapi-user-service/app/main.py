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