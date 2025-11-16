from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy import select

from src.db.utils import SessionLocal
from src.models.users import Session


def session_authenticate(key: str = Depends(APIKeyHeader(name='Authorization'))):
    invalid_token_error = HTTPException(status_code=401, detail="Invalid token")
    if not key.startswith("Bearer "):
        raise invalid_token_error

    key = key.split(" ")[1]

    with SessionLocal() as session:
        user_session = session.scalar(select(Session).where(Session.session_key == key))
        if not user_session:
            raise invalid_token_error

        return user_session.user
