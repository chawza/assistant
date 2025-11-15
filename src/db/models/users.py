import os
import secrets
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime, timedelta
import hashlib

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'auth__users'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(50), default='')

    def set_password(self, password: str):
        self.password = self._hash_password(password)

    def check_password(self, password: str):
        return self.password == self._hash_password(password)

    def _hash_password(self, password: str):
        _salt = str(os.environ.get('ASSISTANT_MASTER_SECRET', ''))
        if not _salt:
            raise ValueError("ASSISTANT_MASTER_SECRET environment variable is not set")
        salt = _salt.encode('utf-8')

        return hashlib.sha256(salt + password.encode('utf-8')).hexdigest()


class Session(Base):
    __tablename__ = 'auth__sessions'

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("auth__users.id"))
    session_key: Mapped[str] = mapped_column(String(64), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now() + timedelta(days=7))

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session_key = self._generate_session_key()

    def _generate_session_key(self) -> str:
        return secrets.token_urlsafe(32)

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
