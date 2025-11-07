import asyncio
from app.api.auth_new import router
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.utils.database import get_db
from sqlalchemy.orm import Session
from unittest.mock import MagicMock

# Create a mock database session
def override_get_db():
    mock_db = MagicMock(spec=Session)
    return mock_db

# Create a test app with just the auth routes
app = FastAPI()
app.include_router(router)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Print all registered routes
from fastapi.routing import APIRoute
for route in app.routes:
    if isinstance(route, APIRoute):
        print(f"Method: {route.methods}, Path: {route.path}")
    else:
        print(f"Route: {route}")

def test_register():
    response = client.post("/auth/register", json={
        "email": "testuser@gmail.com",
        "password": "testpassword123"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_register()