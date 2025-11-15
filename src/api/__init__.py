from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.utils import get_session
from src.api.middleware.session import validate_session
from src.db.models.users import Session as UserSession


SessionDep = Annotated[Session, Depends(get_session)]
CurrentSession = Annotated[UserSession, Depends(validate_session)]
