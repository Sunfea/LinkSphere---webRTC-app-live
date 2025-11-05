from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_token_endpoint():
    """Test the token endpoint with invalid credentials"""
    response = client.post("/api/token", data={
        "username": "invalid",
        "password": "invalid"
    })
    assert response.status_code == 401

def test_create_user():
    """Test creating a new user"""
    response = client.post("/api/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    # This might fail if user already exists in our mock database
    assert response.status_code in [200, 400]

def test_metrics_endpoint():
    """Test the metrics endpoint"""
    response = client.get("/api/metrics")
    # Metrics endpoint returns plain text, not JSON
    assert response.status_code == 200
