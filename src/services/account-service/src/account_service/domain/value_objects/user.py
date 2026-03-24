from __future__ import annotations
from dataclasses import dataclass
import re

import hashlib

from account_service.domain.exceptions import ValidationDomainError

_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if not _EMAIL_PATTERN.fullmatch(self.value):
            raise ValidationDomainError("email invalido")



@dataclass(frozen=True)
class PasswordHash:
    value: str

    @staticmethod
    def from_plain(password: str) -> PasswordHash:
        if len(password) < 8:
            raise ValidationDomainError("senha deve ter ao menos 8 caracteres")
        digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return PasswordHash(digest)

    def matches(self, raw_password: str) -> bool:
        digest = hashlib.sha256(raw_password.encode("utf-8")).hexdigest()
        return digest == self.value