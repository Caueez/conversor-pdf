
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from account_service.infra.observability.logging import setup_logging

from account_service.infra.container import ContainerService
from account_service.settings import get_settings

import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    
    settings = get_settings()
    setup_logging(logging.DEBUG if settings.DEBUG else logging.INFO)
    container = ContainerService.build(settings)
    await container.startup()

    app.state.container = container

    try:
        yield
    
    finally:
        await container.shutdown()