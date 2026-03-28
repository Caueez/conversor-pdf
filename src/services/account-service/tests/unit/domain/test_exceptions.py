from __future__ import annotations

import pytest

from account_service.domain.exceptions import (
    AuthenticationDomainError,
    AuthorizationDomainError,
    ConflictDomainError,
    DomainError,
    EntityNotFoundError,
    ValidationDomainError,
)


pytestmark = pytest.mark.unit


def test_domain_exception_hierarchy() -> None:
    assert issubclass(ValidationDomainError, DomainError)
    assert issubclass(EntityNotFoundError, DomainError)
    assert issubclass(ConflictDomainError, DomainError)
    assert issubclass(AuthenticationDomainError, DomainError)
    assert issubclass(AuthorizationDomainError, DomainError)
