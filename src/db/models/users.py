import os
from sqlmodel import Field, SQLModel
import hashlib

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(title="Email", description="The email address of the user", unique=True)
    password: str = Field(title="Password", description="The password of the user", default="")

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
