from __future__ import annotations
from dataclasses import dataclass
import re

from account_service.domain.exceptions import ValidationDomainError

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not _EMAIL_PATTERN.fullmatch(self.value):
            raise ValidationDomainError("Email is not valid")
        

@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self) -> None:
        if len(self.value) < 8:
            raise ValidationDomainError("Password must be at least 8 characters long")

        if len(self.value) > 72:
            raise ValidationDomainError("Password must be at most 72 characters long")