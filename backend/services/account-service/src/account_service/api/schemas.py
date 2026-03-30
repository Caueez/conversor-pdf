from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=72)


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=120)
    email: Optional[str] = Field(default=None, min_length=5, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8, max_length=72)

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> UpdateUserRequest:
        if all(value is None for value in (self.name, self.email, self.password)):
            raise ValueError("At least one field must be provided for update")
        return self


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    created_at: str
    updated_at: str


class LoginRequest(BaseModel):
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=72)


class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_expires_at: str
    refresh_expires_at: str
