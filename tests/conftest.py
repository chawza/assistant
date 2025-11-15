import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.db.models import Base
from src.db.models.users import User, Session as UserSession

from src.db.models import Base
from src.db.models.users import User, Session as UserSession




pytest_plugins = [
    "tests.fixtures.user"
]


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new database session for a test.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
