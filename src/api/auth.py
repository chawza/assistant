from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.schemas import AuthResponse, ErrorResponse, LoginForm
from src.api.utils import session_authenticate
from src.models.users import User, Session as UserSession
from src.db.utils import get_db_session


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=AuthResponse, responses={401: {"model": ErrorResponse}})
def login(form: LoginForm, db_session: Annotated[Session, Depends(get_db_session)]):
    user = db_session.scalar(select(User).where(User.email == form.email))

    if not user or not user.check_password(form.password):
        return ErrorResponse(
            details=["Invalid email or password"]
        )

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

@router.get('/check')
async def check_session(user: Annotated[User, Depends(session_authenticate)]):
    return {
        'user': {
            'email': user.email
        }
    }
