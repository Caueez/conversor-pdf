
from typing import Any, Optional

from dataclasses import dataclass

from collections import defaultdict

from enum import Enum

class Statement(Enum):
    SELECT: str = "SELECT"
    INSERT: str = "INSERT"
    UPDATE: str = "UPDATE"
    DELETE: str = "DELETE"


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
    statement: Statement
    query: str
    values: Optional[list[object]]

    @classmethod
    def create(cls, statement: str, query: str, values: Optional[list[object]] = None):
        statement = Statement(statement.upper())
        if not cls._is_valide_query(statement, query):
            raise RuntimeError("Invalid query")
        return cls(statement, query, values)
    
    @classmethod
    def _is_valide_query(cls, statement: Statement, query: str) -> bool:
        if statement.value != query.split(" ")[0]:
            raise RuntimeError("Invalid query")
        
        return True
    