
from typing import Any, Optional

from dataclasses import dataclass

from collections import defaultdict

from enum import Enum

class Statement(Enum):
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


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
        statement_enum = Statement(statement.upper())
        if not cls._is_valide_query(statement_enum, query):
            raise RuntimeError("Invalid query")
        return cls(statement_enum, query, values)
    
    @classmethod
    def _is_valide_query(cls, statement: Statement, query: str) -> bool:
        first_word = query.lstrip().split(None, 1)[0].upper()
        if statement.value != first_word:
            raise RuntimeError("Invalid query")

        
        return True
    
