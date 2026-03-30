from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from account_service.domain.exceptions import AuthenticationDomainError
from account_service.infra.security.jwt_token_service_adapter import JwtTokenServiceAdapter


pytestmark = pytest.mark.unit


def test_issue_and_decode_access_and_refresh_tokens() -> None:
    adapter = JwtTokenServiceAdapter(secret="test-secret", algorithm="HS256")
    now = datetime.now(tz=UTC)

    access_token = adapter.issue_access_token(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        expires_at=now + timedelta(hours=1),
    )
    refresh_token = adapter.issue_refresh_token(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        token_id="d7aec2a4-c545-47e0-a5a4-7ec882bc8ea8",
        expires_at=now + timedelta(days=7),
    )

    access_payload = adapter.decode_access_token(access_token)
    refresh_payload = adapter.decode_refresh_token(refresh_token)

    assert access_payload.type == "access"
    assert access_payload.sub == "31cb2264-07a5-4d53-a758-05476fd48341"
    assert access_payload.session_id == "2cad4693-7fe2-4d6d-b235-95e06f6e4368"

    assert refresh_payload.type == "refresh"
    assert refresh_payload.jti == "d7aec2a4-c545-47e0-a5a4-7ec882bc8ea8"


def test_decode_rejects_tampered_token() -> None:
    adapter = JwtTokenServiceAdapter(secret="test-secret", algorithm="HS256")
    token = adapter.issue_access_token(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        expires_at=datetime.now(tz=UTC) + timedelta(minutes=15),
    )

    parts = token.split(".")
    tampered = f"{parts[0]}.{parts[1]}.invalid-signature"

    with pytest.raises(AuthenticationDomainError, match="Invalid token"):
        adapter.decode_access_token(tampered)


def test_decode_rejects_expired_token() -> None:
    adapter = JwtTokenServiceAdapter(secret="test-secret", algorithm="HS256")
    expired_token = adapter.issue_access_token(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        expires_at=datetime.now(tz=UTC) - timedelta(seconds=1),
    )

    with pytest.raises(AuthenticationDomainError, match="Token expired"):
        adapter.decode_access_token(expired_token)


def test_decode_rejects_wrong_token_type() -> None:
    adapter = JwtTokenServiceAdapter(secret="test-secret", algorithm="HS256")
    refresh_token = adapter.issue_refresh_token(
        user_id="31cb2264-07a5-4d53-a758-05476fd48341",
        session_id="2cad4693-7fe2-4d6d-b235-95e06f6e4368",
        token_id="d7aec2a4-c545-47e0-a5a4-7ec882bc8ea8",
        expires_at=datetime.now(tz=UTC) + timedelta(days=7),
    )

    with pytest.raises(AuthenticationDomainError, match="Invalid access token"):
        adapter.decode_access_token(refresh_token)
