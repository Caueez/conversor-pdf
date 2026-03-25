
from fastapi import FastAPI

from account_service.api.lifespan import lifespan

from account_service.api.routes.routers import build_routers

import logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Conversor de PDF",
        lifespan=lifespan
    )
    
    app.include_router(build_routers())


    # TODO: Add exceptions
    # @app.ex


    return app