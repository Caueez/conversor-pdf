from fastapi import APIRouter, Depends

from account_service.api.dependencies import get_admin_session
from account_service.api.routes.session import router as session_router
from account_service.api.routes.user import router as user_router


def build_routers() -> APIRouter:
    router = APIRouter()

    router.include_router(session_router)
    router.include_router(user_router, dependencies=[Depends(get_admin_session)])

    return router
