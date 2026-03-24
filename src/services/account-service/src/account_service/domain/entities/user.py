
from dataclasses import dataclass, field

from account_service.shared.typed import utc_now, new_uuid

from datetime import datetime


@dataclass(frozen=True)
class User:
    name: str
    email: str
    password_hash: str
    id: str = field(default_factory=new_uuid)
    is_active: bool = True
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, str | datetime | bool]:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def compare_hash(self, hash: str):
        return self.password_hash == hash
