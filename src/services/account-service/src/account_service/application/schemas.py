from typing import Optional

from pydantic import BaseModel



class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str


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
