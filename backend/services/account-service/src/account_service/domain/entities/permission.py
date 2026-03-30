from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from account_service.shared.typed import new_uuid, utc_now


PERMISSION_USERS_MANAGE = "users:manage"


@dataclass(frozen=True)
class Permission:
    key: str
    description: str
    id: str = field(default_factory=new_uuid)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
