from fastapi import FastAPI

from account_service.api.exception_handlers import register_exception_handlers
from account_service.api.lifespan import lifespan
from account_service.api.routes.routers import build_routers


def create_app() -> FastAPI:
    app = FastAPI(title="Conversor de PDF", lifespan=lifespan)

    app.include_router(build_routers())
    register_exception_handlers(app)

    return app
