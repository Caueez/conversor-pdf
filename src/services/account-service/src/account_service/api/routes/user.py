from typing import Annotated

from fastapi import APIRouter, Depends, status

from account_service.api.dependencies import get_container, get_trace_id
from account_service.infra.container import ContainerService
from account_service.api.schemas import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from account_service.application.schemas import (
    CreateUserDTO,
    DeleteUserDTO,
    UpdateUserDTO,
)

from account_service.api.presenters.user_presenter import dto_to_user_response, request_to_dto

router = APIRouter(tags=["Users"])
ContainerDep = Annotated[ContainerService, Depends(get_container)]
TraceIdDep = Annotated[str, Depends(get_trace_id)]


@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> list[UserResponse]:
    application_dtos = await container.users.list()
    return [dto_to_user_response(dto) for dto in application_dtos]


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_request: CreateUserRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> UserResponse:
    request_dto: CreateUserDTO = request_to_dto(CreateUserDTO, **user_request.model_dump(exclude_none=True))
    dto = await container.users.create(request_dto)
    return dto_to_user_response(dto)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> None:
    request_dto: DeleteUserDTO = request_to_dto(DeleteUserDTO, user_id=user_id)
    await container.users.delete(request_dto)
    


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_request: UpdateUserRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> UserResponse:
    request_dto: UpdateUserDTO = request_to_dto(UpdateUserDTO, user_id=user_id, **user_request.model_dump(exclude_none=True))
    response_dto = await container.users.update(request_dto)
    return dto_to_user_response(response_dto)
