from __future__ import annotations

import pytest
from fastapi import FastAPI

from account_service.main import app


pytestmark = pytest.mark.unit


def test_main_exports_fastapi_application() -> None:
    assert isinstance(app, FastAPI)
