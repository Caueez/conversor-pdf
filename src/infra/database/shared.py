
from typing import Any, Optional

from dataclasses import dataclass

from collections import defaultdict


@dataclass(frozen=True)
class DatabaseRow:
    values: dict[str, Any]

    @classmethod
    def create(cls, record: dict[str, Any]):
        values: dict[str, Any] = defaultdict(lambda: None)
        for key, value in record.items():
            values[key] = value
        
        return cls(values)

    def __getitem__(self, key: str):
        return self.values[key]
    

@dataclass(frozen=True)
class Query:
    query: str
    values: Optional[list[object]]