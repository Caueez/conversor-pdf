from __future__ import annotations

import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime
from typing import Any

from pydantic import ValidationError

from account_service.application.interfaces.token_service import TokenServicePort
from account_service.application.schemas import AccessTokenPayloadDTO, RefreshTokenPayloadDTO
from account_service.domain.exceptions import AuthenticationDomainError


class JwtTokenServiceAdapter(TokenServicePort):
    def __init__(self, *, secret: str, algorithm: str = "HS256") -> None:
        if algorithm != "HS256":
            raise ValueError("Only HS256 algorithm is supported")

        if not secret:
            raise ValueError("JWT secret cannot be empty")

        self._algorithm = algorithm
        self._secret = secret.encode()

    def issue_access_token(self, *, user_id: str, session_id: str, expires_at: datetime) -> str:
        claims = {
            "sub": user_id,
            "session_id": session_id,
            "type": "access",
            "exp": int(expires_at.timestamp()),
        }
        return self._encode(claims)

    def issue_refresh_token(
        self,
        *,
        user_id: str,
        session_id: str,
        token_id: str,
        expires_at: datetime,
    ) -> str:
        claims = {
            "sub": user_id,
            "session_id": session_id,
            "jti": token_id,
            "type": "refresh",
            "exp": int(expires_at.timestamp()),
        }
        return self._encode(claims)

    def decode_access_token(self, token: str) -> AccessTokenPayloadDTO:
        payload = self._decode(token)
        try:
            parsed = AccessTokenPayloadDTO.model_validate(payload)
        except ValidationError as exc:
            raise AuthenticationDomainError("Invalid access token") from exc

        if parsed.type != "access":
            raise AuthenticationDomainError("Invalid access token")

        return parsed

    def decode_refresh_token(self, token: str) -> RefreshTokenPayloadDTO:
        payload = self._decode(token)
        try:
            parsed = RefreshTokenPayloadDTO.model_validate(payload)
        except ValidationError as exc:
            raise AuthenticationDomainError("Invalid refresh token") from exc

        if parsed.type != "refresh":
            raise AuthenticationDomainError("Invalid refresh token")

        return parsed

    def _encode(self, payload: dict[str, Any]) -> str:
        header = {"alg": self._algorithm, "typ": "JWT"}
        encoded_header = self._b64url_encode(json.dumps(header, separators=(",", ":")).encode())
        encoded_payload = self._b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
        signing_input = f"{encoded_header}.{encoded_payload}".encode()
        signature = hmac.new(self._secret, signing_input, hashlib.sha256).digest()
        encoded_signature = self._b64url_encode(signature)
        return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

    def _decode(self, token: str) -> dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 3:
            raise AuthenticationDomainError("Invalid token")

        encoded_header, encoded_payload, encoded_signature = parts
        signing_input = f"{encoded_header}.{encoded_payload}".encode()
        expected_signature = hmac.new(self._secret, signing_input, hashlib.sha256).digest()
        try:
            provided_signature = self._b64url_decode(encoded_signature)
        except ValueError as exc:
            raise AuthenticationDomainError("Invalid token") from exc

        if not hmac.compare_digest(expected_signature, provided_signature):
            raise AuthenticationDomainError("Invalid token")

        try:
            header = json.loads(self._b64url_decode(encoded_header))
            payload = json.loads(self._b64url_decode(encoded_payload))
        except (ValueError, json.JSONDecodeError) as exc:
            raise AuthenticationDomainError("Invalid token") from exc

        if header.get("alg") != self._algorithm or header.get("typ") != "JWT":
            raise AuthenticationDomainError("Invalid token")

        exp = payload.get("exp")
        if not isinstance(exp, int):
            raise AuthenticationDomainError("Invalid token")

        now = int(datetime.now(tz=UTC).timestamp())
        if exp <= now:
            raise AuthenticationDomainError("Token expired")

        return payload

    def _b64url_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    def _b64url_decode(self, data: str) -> bytes:
        padding = "=" * (-len(data) % 4)
        return base64.urlsafe_b64decode((data + padding).encode("ascii"))
