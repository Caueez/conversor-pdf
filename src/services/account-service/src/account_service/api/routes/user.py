from uuid import uuid4

from fastapi import APIRouter, Depends, Request

from fastapi.responses import JSONResponse

from account_service.infra.container import ContainerService

from account_service.api.schemas import (
    CreateUserRequest,
    DeleteUserRequest
)

from account_service.application.schemas import (
    CreateUserDTO,
    DeleteUserDTO
)

router = APIRouter()

def get_container(request: Request) -> ContainerService:
    return request.app.state.container

def get_trace_id(request: Request) -> str:
    trace_id = request.headers.get("x-trace-id")
    if trace_id:
        return trace_id
    return str(uuid4())


@router.get("/")
async def list_users(
        trace_id: str = Depends(get_trace_id),
        container: ContainerService = Depends(get_container)
):
    try:
        users_dto = await container.users.list()
        json_response = [user.model_dump() for user in users_dto]
        return JSONResponse(status_code=200, content=json_response)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@router.post("/")
async def create_user(
        user_request: CreateUserRequest,
        trace_id: str = Depends(get_trace_id),
        container: ContainerService = Depends(get_container)
):
    try:
        dto = CreateUserDTO.model_validate(user_request.model_dump())
        user_dto = await container.users.create(dto)
        json_response = user_dto.model_dump()
        return JSONResponse(status_code=201, content=json_response)
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

@router.delete("/{user_id}")
async def delete_user(
    user_request: DeleteUserRequest,
    trace_id: str = Depends(get_trace_id),
    container: ContainerService = Depends(get_container)
):
    try:
        dto = DeleteUserDTO.model_validate(user_request.model_dump())
        await container.users.delete(dto)
        return JSONResponse(status_code=200, content={"message": "User deleted"})
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": str(e)})

