import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.server import app
from src.db.utils import get_db_session
from src.db.models.users import User


# The user fixture is automatically discovered by pytest from tests/fixtures/user.py
# The db_session fixture is automatically discovered by pytest from tests/conftest.py

@pytest.fixture
def client(db_session: Session):
    """
    Provides a test client for the FastAPI application, with the database
    session dependency overridden to use the in-memory test database.
    """
    def override_get_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_login_success(client: TestClient, user: User):
    """
    Tests that a user can successfully log in with correct credentials.
    """
    response = client.post(
        "/api/auth/login",
        json={"email": user.email, "password": user.raw_password}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["email"] == user.email
    assert data["user"]["id"] == user.id
