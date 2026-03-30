from typing import Optional

from pydantic import BaseModel
from account_service.domain.entities.role import ROLE_KEY_USER


class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str
    role: str = ROLE_KEY_USER


class DeleteUserDTO(BaseModel):
    user_id: str

class UpdateUserDTO(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserDTO(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    created_at: str
    updated_at: str


class LoginDTO(BaseModel):
    email: str
    password: str


class SessionTokenPairDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    access_expires_at: str
    refresh_expires_at: str


class AccessTokenPayloadDTO(BaseModel):
    sub: str
    session_id: str
    type: str
    exp: int


class RefreshTokenPayloadDTO(BaseModel):
    sub: str
    session_id: str
    jti: str
    type: str
    exp: int
