import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import Base
from src.db.utils import SessionLocal


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new database session for a test.
    """
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    # Import all models to ensure they're registered with the Base
    # Explicitly import User and Session classes
    from src.db.models.users import User, Session

    # Create all tables
    Base.metadata.create_all(engine)

    # Store original SessionLocal
    original_session_local = SessionLocal

    # Create a sessionmaker bound to the test engine and override SessionLocal
    import src.db.utils
    test_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    src.db.utils.SessionLocal = test_session_local

    session = test_session_local()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
        # Restore original SessionLocal
        src.db.utils.SessionLocal = original_session_local


# Make sure the user fixture plugin is loaded
pytest_plugins = [
    "tests.fixtures.user"
]