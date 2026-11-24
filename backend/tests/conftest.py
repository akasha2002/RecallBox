import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.db.session import SessionLocal


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """Provides a TestClient instance for API integration testing."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Provides a live database session that rolls back changes after each test."""
    if SessionLocal is None:
        pytest.skip("Database is not configured for session tests.")
    
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
