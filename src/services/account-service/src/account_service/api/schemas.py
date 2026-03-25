from pydantic import BaseModel

from typing import Optional

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

class DeleteUserRequest(BaseModel):
    user_id: str

class UpdateUserRequest(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None