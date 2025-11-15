from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select

from src.api import SessionDep, CurrentSession
from src.db.models.users import User, Session as UserSession


router = APIRouter(
    tags=['Authentication']
)

class UserSchema(BaseModel):
    id: int
    email: str

class AuthResponse(BaseModel):
    token: str
    user: UserSchema

class LoginForm(BaseModel):
    email: str
    password: str


@router.post('/login', response_model=AuthResponse)
def login(form: LoginForm, db_session: SessionDep):
    user = db_session.scalar(select(User).where(User.email == form.email))

    if not user or not user.check_password(form.password):
        raise HTTPException(status_code=400, detail='Invalid email or password')

    # Create a new session
    user_session = UserSession(user_id=user.id)
    db_session.add(user_session)
    db_session.commit()
    db_session.refresh(user_session)

    return {
        'token': user_session.session_key,
        'user': {
            'id': user.id,
            'email': user.email
        }
    }
