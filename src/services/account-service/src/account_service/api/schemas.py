from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str

class DeleteUserRequest(BaseModel):
    user_id: str