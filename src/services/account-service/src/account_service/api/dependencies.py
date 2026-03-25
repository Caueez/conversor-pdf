from fastapi import Request

from account_service.infra.container import ContainerService
from account_service.shared.typed import new_uuid


def get_container(request: Request) -> ContainerService:
    return request.app.state.container

def get_trace_id(request: Request) -> str:
    trace_id = getattr(request.state, "trace_id", None) or request.headers.get("x-trace-id")
    if trace_id:
        return trace_id
    return new_uuid()
