from __future__ import annotations

from datetime import datetime
from typing import Protocol

from account_service.application.schemas import AccessTokenPayloadDTO, RefreshTokenPayloadDTO


class TokenServicePort(Protocol):
    def issue_access_token(self, *, user_id: str, session_id: str, expires_at: datetime) -> str: ...

    def issue_refresh_token(
        self,
        *,
        user_id: str,
        session_id: str,
        token_id: str,
        expires_at: datetime,
    ) -> str: ...

    def decode_access_token(self, token: str) -> AccessTokenPayloadDTO: ...

    def decode_refresh_token(self, token: str) -> RefreshTokenPayloadDTO: ...
