from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from account_service.infra.container import ContainerService
from account_service.settings import get_settings

from account_service.api.routes.routers import build_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    
    settings = get_settings()
    container = ContainerService.build(settings)
    await container.startup()

    app.state.container = container

    yield

    await container.shutdown()



def create_app() -> FastAPI:
    app = FastAPI(
        title="Conversor de PDF",
        lifespan=lifespan
    )
    
    app.include_router(build_routers())


    # TODO: Add exceptions
    # @app.ex


    return app