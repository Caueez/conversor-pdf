from __future__ import annotations

from datetime import datetime, timedelta
from uuid import UUID

from account_service.application.interfaces.repository import SessionRepositoryPort
from account_service.application.interfaces.token_service import TokenServicePort
from account_service.application.schemas import (
    AccessTokenPayloadDTO,
    CreateUserDTO,
    LoginDTO,
    SessionTokenPairDTO,
    UserDTO,
)
from account_service.application.services.authorization_service import AuthorizationService
from account_service.application.services.user_service import UserService
from account_service.domain.entities.permission import PERMISSION_USERS_MANAGE
from account_service.domain.entities.session import Session
from account_service.domain.exceptions import AuthenticationDomainError, AuthorizationDomainError
from account_service.domain.entities.user import User
from account_service.shared.typed import new_uuid, utc_now


class SessionUseCase:
    def __init__(
        self,
        user_service: UserService,
        authorization_service: AuthorizationService,
        session_repository: SessionRepositoryPort,
        token_service: TokenServicePort,
        *,
        access_ttl: timedelta,
        refresh_ttl: timedelta,
    ) -> None:
        self._user_service = user_service
        self._authorization_service = authorization_service
        self._session_repository = session_repository
        self._token_service = token_service
        self._access_ttl = access_ttl
        self._refresh_ttl = refresh_ttl

    async def register(self, dto: CreateUserDTO) -> SessionTokenPairDTO:
        user = await self._user_service.create(dto)
        return await self._create_token_pair_for_user(user)

    async def login(self, dto: LoginDTO) -> SessionTokenPairDTO:
        user = await self._user_service.authenticate(dto)
        if not user:
            raise AuthenticationDomainError("Invalid credentials")

        return await self._create_token_pair_for_user(user)

    async def login_admin(self, dto: LoginDTO) -> SessionTokenPairDTO:
        user = await self._user_service.authenticate(dto)
        if not user:
            raise AuthenticationDomainError("Invalid credentials")

        can_manage_users = await self._authorization_service.has_permission(
            user.role,
            PERMISSION_USERS_MANAGE,
        )
        if not can_manage_users:
            raise AuthorizationDomainError("Admin credentials are required")

        return await self._create_token_pair_for_user(user)

    async def refresh(self, refresh_token: str) -> SessionTokenPairDTO:
        payload = self._token_service.decode_refresh_token(refresh_token)

        session_id = self._to_uuid(payload.session_id)
        user_id = self._to_uuid(payload.sub)

        session = await self._session_repository.get(session_id)
        if not session:
            raise AuthenticationDomainError("Invalid refresh token")

        now = utc_now()
        if session.revoked or session.expires_at <= now:
            raise AuthenticationDomainError("Invalid refresh token")

        if str(session.user_id) != str(user_id):
            raise AuthenticationDomainError("Invalid refresh token")

        if session.token_id != payload.jti:
            raise AuthenticationDomainError("Invalid refresh token")

        user = await self._user_service.get_active_by_id(user_id)
        if not user:
            raise AuthenticationDomainError("Invalid refresh token")

        next_refresh_token_id = new_uuid()
        next_refresh_expires_at = now + self._refresh_ttl
        await self._session_repository.rotate(session_id, next_refresh_token_id, next_refresh_expires_at)

        return self._build_token_pair(
            user_id=str(user.id),
            session_id=str(session.id),
            refresh_token_id=next_refresh_token_id,
            now=now,
            refresh_expires_at=next_refresh_expires_at,
        )

    async def authenticate_access_token(self, access_token: str) -> AccessTokenPayloadDTO:
        payload = self._token_service.decode_access_token(access_token)

        session_id = self._to_uuid(payload.session_id)
        user_id = self._to_uuid(payload.sub)

        session = await self._session_repository.get(session_id)
        if not session:
            raise AuthenticationDomainError("Session is not active")

        if session.revoked:
            raise AuthenticationDomainError("Session is not active")

        if session.expires_at <= utc_now():
            raise AuthenticationDomainError("Session is not active")

        if str(session.user_id) != str(user_id):
            raise AuthenticationDomainError("Session is not active")

        user = await self._user_service.get_active_by_id(user_id)
        if not user:
            raise AuthenticationDomainError("Session is not active")

        return payload

    async def logout(self, access_token: str) -> None:
        payload = await self.authenticate_access_token(access_token)
        session_id = self._to_uuid(payload.session_id)
        await self._session_repository.revoke(session_id)

    async def me(self, access_token: str) -> UserDTO:
        payload = await self.authenticate_access_token(access_token)
        user_id = self._to_uuid(payload.sub)

        user = await self._user_service.get_active_by_id(user_id)
        if not user:
            raise AuthenticationDomainError("Session is not active")

        return UserDTO.model_validate(user.to_dict())

    async def _create_token_pair_for_user(self, user: User) -> SessionTokenPairDTO:
        now = utc_now()
        session = Session(
            user_id=str(user.id),
            token_id=new_uuid(),
            expires_at=now + self._refresh_ttl,
        )
        await self._session_repository.create(session)

        return self._build_token_pair(
            user_id=str(user.id),
            session_id=str(session.id),
            refresh_token_id=session.token_id,
            now=now,
            refresh_expires_at=session.expires_at,
        )

    def _build_token_pair(
        self,
        *,
        user_id: str,
        session_id: str,
        refresh_token_id: str,
        now: datetime,
        refresh_expires_at: datetime,
    ) -> SessionTokenPairDTO:
        access_expires_at = now + self._access_ttl

        access_token = self._token_service.issue_access_token(
            user_id=user_id,
            session_id=session_id,
            expires_at=access_expires_at,
        )
        refresh_token = self._token_service.issue_refresh_token(
            user_id=user_id,
            session_id=session_id,
            token_id=refresh_token_id,
            expires_at=refresh_expires_at,
        )

        return SessionTokenPairDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            access_expires_at=access_expires_at.isoformat(),
            refresh_expires_at=refresh_expires_at.isoformat(),
        )

    def _to_uuid(self, value: str) -> UUID:
        try:
            return UUID(value)
        except ValueError as exc:
            raise AuthenticationDomainError("Invalid token payload") from exc
