from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from starlette.requests import Request

import account_service.api.dependencies as dependencies_module
from account_service.api.dependencies import get_container, get_trace_id


pytestmark = pytest.mark.unit


def _build_request(
    *,
    app: FastAPI | None = None,
    headers: list[tuple[bytes, bytes]] | None = None,
) -> Request:
    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "GET",
        "path": "/",
        "headers": headers or [],
        "app": app or FastAPI(),
    }
    return Request(scope)


def test_get_container_reads_container_from_app_state() -> None:
    app = FastAPI()
    container = object()
    app.state.container = container
    request = _build_request(app=app)

    assert get_container(request) is container


def test_get_trace_id_prefers_request_state() -> None:
    request = _build_request(headers=[(b"x-trace-id", b"header-trace-id")])
    request._state = SimpleNamespace(trace_id="state-trace-id")  # noqa: SLF001

    assert get_trace_id(request) == "state-trace-id"


def test_get_trace_id_uses_header_when_state_is_missing() -> None:
    request = _build_request(headers=[(b"x-trace-id", b"header-trace-id")])

    assert get_trace_id(request) == "header-trace-id"


def test_get_trace_id_generates_value_when_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dependencies_module, "new_uuid", lambda: "generated-trace-id")
    request = _build_request()

    assert get_trace_id(request) == "generated-trace-id"
