from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "API REST para la predicción del porcentaje "
            "de blanqueamiento de corales."
        ),
    )

    application.include_router(router)

    return application


app = create_app()