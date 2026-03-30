from __future__ import annotations

from datetime import UTC
from uuid import UUID

import pytest

from account_service.domain.entities.permission import Permission
from account_service.domain.entities.role import Role
from account_service.domain.entities.role_permission import RolePermission


pytestmark = pytest.mark.unit


def test_role_entity_defaults() -> None:
    role = Role(key="admin", name="Administrator")

    UUID(role.id)
    assert role.created_at.tzinfo is UTC
    assert role.updated_at.tzinfo is UTC


def test_permission_entity_defaults() -> None:
    permission = Permission(key="users:manage", description="Manage users")

    UUID(permission.id)
    assert permission.created_at.tzinfo is UTC
    assert permission.updated_at.tzinfo is UTC


def test_role_permission_entity_defaults() -> None:
    role_permission = RolePermission(role_id="role-id", permission_id="permission-id")
    assert role_permission.role_id == "role-id"
    assert role_permission.permission_id == "permission-id"
    assert role_permission.created_at.tzinfo is UTC
