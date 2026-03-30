from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from account_service.application.schemas import AccessTokenPayloadDTO
from account_service.domain.entities.permission import PERMISSION_USERS_MANAGE
from account_service.domain.exceptions import AuthenticationDomainError, AuthorizationDomainError
from account_service.infra.container import ContainerService
from account_service.shared.typed import new_uuid

bearer_scheme = HTTPBearer(auto_error=False, scheme_name="BearerAuth")


def get_container(request: Request) -> ContainerService:
    return request.app.state.container


def get_trace_id(request: Request) -> str:
    trace_id = getattr(request.state, "trace_id", None) or request.headers.get("x-trace-id")
    if trace_id:
        return trace_id
    return new_uuid()


def get_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Security(bearer_scheme)],
) -> str:
    if credentials is None:
        raise AuthenticationDomainError("Authentication required")

    if credentials.scheme.lower() != "bearer" or not credentials.credentials:
        raise AuthenticationDomainError("Invalid authorization header")

    return credentials.credentials


@dataclass(frozen=True)
class AuthenticatedSession:
    user_id: str
    session_id: str
    role: str


async def get_authenticated_session(
    request: Request,
    token: Annotated[str, Depends(get_bearer_token)],
) -> AuthenticatedSession:
    container = get_container(request)
    payload: AccessTokenPayloadDTO = await container.sessions.authenticate_access_token(token)
    user = await container.user_service.get_active_by_id(UUID(payload.sub))
    if not user:
        raise AuthenticationDomainError("Session is not active")

    return AuthenticatedSession(
        user_id=payload.sub,
        session_id=payload.session_id,
        role=user.role,
    )


async def get_admin_session(
    request: Request,
    session: Annotated[AuthenticatedSession, Depends(get_authenticated_session)],
) -> AuthenticatedSession:
    container = get_container(request)
    can_manage_users = await container.authorization_service.has_permission(
        session.role,
        PERMISSION_USERS_MANAGE,
    )
    if not can_manage_users:
        raise AuthorizationDomainError("Admin privileges are required")
    return session
