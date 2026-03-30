from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from account_service.api.dependencies import get_bearer_token, get_container, get_trace_id
from account_service.api.presenters.session_presenter import dto_to_token_pair_response
from account_service.api.presenters.user_presenter import dto_to_user_response, request_to_dto
from account_service.api.schemas import CreateUserRequest, LoginRequest, TokenPairResponse, UserResponse
from account_service.application.schemas import CreateUserDTO, LoginDTO
from account_service.infra.container import ContainerService

router = APIRouter(prefix="/session", tags=["Session"])
ContainerDep = Annotated[ContainerService, Depends(get_container)]
TraceIdDep = Annotated[str, Depends(get_trace_id)]
BearerTokenDep = Annotated[str, Depends(get_bearer_token)]


@router.post("/login", response_model=TokenPairResponse, status_code=status.HTTP_200_OK)
async def login(
    request: LoginRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> TokenPairResponse:
    dto: LoginDTO = request_to_dto(LoginDTO, **request.model_dump(exclude_none=True))
    response_dto = await container.sessions.login(dto)
    return dto_to_token_pair_response(response_dto)


@router.post("/admin/login", response_model=TokenPairResponse, status_code=status.HTTP_200_OK)
async def login_admin(
    request: LoginRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> TokenPairResponse:
    dto: LoginDTO = request_to_dto(LoginDTO, **request.model_dump(exclude_none=True))
    response_dto = await container.sessions.login_admin(dto)
    return dto_to_token_pair_response(response_dto)


@router.post("/register", response_model=TokenPairResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: CreateUserRequest,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> TokenPairResponse:
    dto: CreateUserDTO = request_to_dto(CreateUserDTO, **request.model_dump(exclude_none=True))
    response_dto = await container.sessions.register(dto)
    return dto_to_token_pair_response(response_dto)


@router.post("/refresh", response_model=TokenPairResponse, status_code=status.HTTP_200_OK)
async def refresh(
    token: BearerTokenDep,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> TokenPairResponse:
    response_dto = await container.sessions.refresh(token)
    return dto_to_token_pair_response(response_dto)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: BearerTokenDep,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> None:
    await container.sessions.logout(token)


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def me(
    token: BearerTokenDep,
    _trace_id: TraceIdDep,
    container: ContainerDep,
) -> UserResponse:
    response_dto = await container.sessions.me(token)
    return dto_to_user_response(response_dto)
