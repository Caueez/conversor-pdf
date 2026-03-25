from fastapi import APIRouter

from account_service.api.routes.user import router as user_router
#from account_service.api.routes.session import router as session_router

def build_routers() -> APIRouter:
    router = APIRouter()
    
    router.include_router(user_router)
    #router.include_router(session_router)

    return router
