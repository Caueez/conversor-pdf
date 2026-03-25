from fastapi import APIRouter, Depends, HTTPException, status

from account_service.api.dependencies import (
    get_container,
    get_trace_id
)

from fastapi.responses import JSONResponse

from account_service.infra.container import ContainerService

from account_service.api.schemas import (
    CreateUserRequest,
    DeleteUserRequest,
    UpdateUserRequest
)

from account_service.application.schemas import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO
)

router = APIRouter()


@router.get("/")
async def list_users(
        trace_id: str = Depends(get_trace_id),
        container: ContainerService = Depends(get_container)
):
    try:
        users_dto = await container.users.list()
        json_response = [user.model_dump() for user in users_dto]
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_response)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})

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
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=json_response)
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})

@router.delete("/{user_id}")
async def delete_user(
    user_request: DeleteUserRequest,
    trace_id: str = Depends(get_trace_id),
    container: ContainerService = Depends(get_container)
):
    try:
        dto = DeleteUserDTO.model_validate(user_request.model_dump())
        await container.users.delete(dto)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User deleted"})
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})

@router.patch("/{user_id}")
async def upload_user(
    user_request: UpdateUserRequest,
    trace_id: str = Depends(get_trace_id),
    container: ContainerService = Depends(get_container)
):
    try:
        dto = UpdateUserDTO.model_validate(user_request.model_dump())
        await container.users.update(dto)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User updated"})
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"message": str(e)})
