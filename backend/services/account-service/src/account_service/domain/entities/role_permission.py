from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from account_service.shared.typed import utc_now


@dataclass(frozen=True)
class RolePermission:
    role_id: str
    permission_id: str
    created_at: datetime = field(default_factory=utc_now)
