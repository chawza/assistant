from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.users import Session as UserSession
from src.db.utils import get_db_session

def get_current_session(session_key: str, db: Session) -> UserSession:
    """Get current session from session key"""
    session = db.scalar(select(UserSession).where(UserSession.session_key == session_key))

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.is_expired():
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")

    return session

def validate_session(request: Request, db: Session = Depends(get_db_session)) -> UserSession:
    """Validate session from request headers"""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    session_key = auth_header.split("Bearer ")[1]
    return get_current_session(session_key, db)
