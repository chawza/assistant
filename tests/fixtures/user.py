import os
import pytest
from sqlalchemy.orm import Session

from src.db.models.users import User


@pytest.fixture
def user(db_session: Session):
    """
    Creates a new user in the database for testing.
    """
    os.environ['ASSISTANT_MASTER_SECRET'] = 'test-secret'
    password = "testpassword"
    user = User(email="test@example.com")
    user.set_password(password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Attach raw password for tests to use
    user.raw_password = password

    return user
