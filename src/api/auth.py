from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from pydantic_core.core_schema import ModelSchema
from sqlmodel import select

from src.api import SessionDep
from src.db.models.users import User


router = APIRouter(
    tags=['Authentication']
)

class UserSchema(BaseModel):
    id: int
    email: str

class AuthResponse(BaseModel):
    token: str
    user: UserSchema


@router.post('/login')
def login(email: str, password: str, session: SessionDep) -> AuthResponse:
    user = session.exec(select(User).where(User.email == email)).first()

    if not user:
        raise HTTPException(status_code=400, detail='Invalid email or password')

    return AuthResponse(
        token='some_token',
        user=UserSchema.model_validate(user.model_dump(include={'id', 'email'}))
    )
