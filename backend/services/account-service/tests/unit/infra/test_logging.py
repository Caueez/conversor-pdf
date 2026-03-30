from __future__ import annotations

import json
import logging
import sys

import pytest

from account_service.infra.observability.logging import JsonFormatter, setup_logging


pytestmark = pytest.mark.unit


def test_json_formatter_serializes_basic_record() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test.logger",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="hello world",
        args=(),
        exc_info=None,
    )

    payload = json.loads(formatter.format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "test.logger"
    assert payload["message"] == "hello world"
    assert "timestamp" in payload


def test_json_formatter_includes_exception_field() -> None:
    formatter = JsonFormatter()
    try:
        raise RuntimeError("boom")
    except RuntimeError:
        record = logging.LogRecord(
            name="test.logger",
            level=logging.ERROR,
            pathname=__file__,
            lineno=20,
            msg="error happened",
            args=(),
            exc_info=True,
        )
        record.exc_info = sys.exc_info()

    payload = json.loads(formatter.format(record))

    assert payload["level"] == "ERROR"
    assert "exception" in payload


def test_setup_logging_replaces_root_handlers() -> None:
    root = logging.getLogger()
    old_handlers = list(root.handlers)
    old_level = root.level

    try:
        setup_logging(logging.DEBUG)
        assert len(root.handlers) == 1
        assert isinstance(root.handlers[0].formatter, JsonFormatter)
        assert root.level == logging.DEBUG
    finally:
        root.handlers.clear()
        root.handlers.extend(old_handlers)
        root.setLevel(old_level)
