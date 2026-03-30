from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from account_service.shared.typed import new_uuid, utc_now


@dataclass(frozen=True)
class Session:
    user_id: str
    token_id: str
    expires_at: datetime
    id: str = field(default_factory=new_uuid)
    revoked: bool = False
    created_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, str | bool]:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "token_id": self.token_id,
            "expires_at": self.expires_at.isoformat(),
            "revoked": self.revoked,
            "created_at": self.created_at.isoformat(),
        }
