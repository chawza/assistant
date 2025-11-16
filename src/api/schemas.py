from pydantic.main import BaseModel


class UserSchema(BaseModel):
    id: int
    email: str

class AuthResponse(BaseModel):
    token: str
    user: UserSchema

class LoginForm(BaseModel):
    email: str
    password: str
