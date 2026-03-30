
from datetime import UTC, datetime

from uuid import uuid4

def utc_now():
    return datetime.now(tz=UTC)

def new_uuid():
    return str(uuid4())