from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Verify that the API root endpoint responds with basic metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "health" in data


def test_v1_health_endpoint():
    """Verify that the /api/v1/health endpoint returns status ok and database connection."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "RecallBox API"
    assert data["version"] == "1.0.0"
    assert data["database"] == "connected"
    assert "timestamp" in data
    assert "environment" in data


def test_root_health_endpoint():
    """Verify that the convenience /health endpoint returns status ok and connected database."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"
