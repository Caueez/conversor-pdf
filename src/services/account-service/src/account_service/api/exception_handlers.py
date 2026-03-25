from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from account_service.domain.exceptions import ConflictDomainError, ValidationDomainError

logger = logging.getLogger(__name__)


def _response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content={"message": message})


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValidationDomainError)
    async def handle_validation_domain_error(_: Request, exc: ValidationDomainError) -> JSONResponse: # pyright: ignore[reportUnusedFunction]
        return _response(status.HTTP_422_UNPROCESSABLE_CONTENT, str(exc))

    @app.exception_handler(ConflictDomainError)
    async def handle_conflict_domain_error(_: Request, exc: ConflictDomainError) -> JSONResponse: # pyright: ignore[reportUnusedFunction]
        return _response(status.HTTP_409_CONFLICT, str(exc))

    @app.exception_handler(ValueError)
    async def handle_value_error(_: Request, __: ValueError) -> JSONResponse: # pyright: ignore[reportUnusedFunction]
        return _response(status.HTTP_400_BAD_REQUEST, "Invalid request data")

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse: # pyright: ignore[reportUnusedFunction]
        logger.exception(
            "Unhandled exception method=%s path=%s",
            request.method,
            request.url.path,
            exc_info=exc,
        )
        return _response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error")
