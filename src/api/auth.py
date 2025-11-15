from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

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


@router.post('/login', response_model=AuthResponse)
def login(email: str, password: str, session: SessionDep):
    result = session.scalar(select(User).where(User.email == email))

    if not result:
        raise HTTPException(status_code=400, detail='Invalid email or password')


    return {
        'token': 'some_token',
        'user': {
            'id': result.id,
            'email': result.email
        }
    }
