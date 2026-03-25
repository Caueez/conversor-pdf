from typing import Annotated

from fastapi import APIRouter, Depends, status

from account_service.api.dependencies import get_container, get_trace_id
from account_service.infra.container import ContainerService
from account_service.api.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
)
from account_service.application.schemas import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO,
    UserDTO,
)

router = APIRouter(tags=["Users"])
ContainerDep = Annotated[ContainerService, Depends(get_container)]
TraceIdDep = Annotated[str, Depends(get_trace_id)]


@router.get("/", response_model=list[UserDTO], status_code=status.HTTP_200_OK)
async def list_users(
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> list[UserDTO]:
    return list(await container.users.list())


@router.post("/", response_model=UserDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_request: CreateUserRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> UserDTO:
    dto = CreateUserDTO.model_validate(user_request.model_dump())
    return await container.users.create(dto)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> None:
    dto = DeleteUserDTO(user_id=user_id)
    await container.users.delete(dto)


@router.patch("/{user_id}", response_model=UserDTO, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_request: UpdateUserRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> UserDTO:
    dto = UpdateUserDTO(user_id=user_id, **user_request.model_dump(exclude_none=True))
    return await container.users.update(dto)
