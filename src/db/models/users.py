import os
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer
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
