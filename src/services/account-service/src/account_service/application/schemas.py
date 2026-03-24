from pydantic import BaseModel



class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str


class UserDTO(BaseModel):
    id: str
    name: str
    email: str
    is_active: bool
    created_at: str
    updated_at: str
