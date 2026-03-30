from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from account_service.shared.typed import new_uuid, utc_now


ROLE_KEY_ADMIN = "admin"
ROLE_KEY_USER = "user"


@dataclass(frozen=True)
class Role:
    key: str
    name: str
    id: str = field(default_factory=new_uuid)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
