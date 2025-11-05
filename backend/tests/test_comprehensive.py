import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.database_models import User, OTP, Room
from datetime import datetime, timedelta
import re

client = TestClient(app)

# Test data
TEST_EMAIL = "testuser@example.com"
TEST_USERNAME = "testuser123"
TEST_PASSWORD = "testpassword"
INVALID_OTP = "000000"
VALID_OTP = "123456"

@pytest.fixture
def db_session():
    """Create a database session for testing"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def cleanup_test_data(db_session):
    """Clean up test data before and after tests"""
    # Clean up before test
    db_session.query(OTP).filter(OTP.email == TEST_EMAIL).delete()
    db_session.query(User).filter(User.email == TEST_EMAIL).delete()
    db_session.commit()
    
    yield
    
    # Clean up after test
    db_session.query(OTP).filter(OTP.email == TEST_EMAIL).delete()
    db_session.query(User).filter(User.email == TEST_EMAIL).delete()
    db_session.commit()

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

def test_metrics_endpoint():
    """Test the metrics endpoint"""
    response = client.get("/api/metrics")
    assert response.status_code == 200

# Auth API Tests
def test_auth_signup_success(cleanup_test_data):
    """Test successful user signup"""
    response = client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    assert response.status_code == 200
    assert "OTP sent to your email" in response.json()["message"]

def test_auth_signup_duplicate_email(cleanup_test_data):
    """Test signup with duplicate email"""
    # First signup
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    
    # Second signup with same email
    response = client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    assert response.status_code == 400
    assert "User with this email already exists" in response.json()["detail"]

def test_auth_signup_invalid_email():
    """Test signup with invalid email"""
    response = client.post("/api/auth/signup", json={"email": "invalid-email"})
    assert response.status_code == 422

def test_auth_verify_otp_success(cleanup_test_data):
    """Test successful OTP verification"""
    # First signup to create user and OTP
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    
    # Get the OTP from database
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    otp_code = otp_record.otp
    db.close()
    
    # Verify OTP
    response = client.post("/api/auth/verify-otp", 
                         json={"email": TEST_EMAIL, "otp": otp_code})
    assert response.status_code == 200
    assert "OTP verified successfully" in response.json()["message"]

def test_auth_verify_otp_invalid(cleanup_test_data):
    """Test OTP verification with invalid OTP"""
    # First signup to create user
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    
    # Verify with invalid OTP
    response = client.post("/api/auth/verify-otp", 
                         json={"email": TEST_EMAIL, "otp": INVALID_OTP})
    assert response.status_code == 400
    assert "Invalid OTP" in response.json()["detail"]

def test_auth_verify_otp_user_not_found():
    """Test OTP verification for non-existent user"""
    response = client.post("/api/auth/verify-otp", 
                         json={"email": "nonexistent@example.com", "otp": VALID_OTP})
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_auth_set_username_success(cleanup_test_data):
    """Test successful username setting"""
    # First signup and verify OTP
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    db.close()
    
    # Set username
    response = client.post("/api/auth/set-username", 
                         json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    assert response.status_code == 200
    assert "Username set successfully" in response.json()["message"]

def test_auth_set_username_invalid_format(cleanup_test_data):
    """Test username setting with invalid format"""
    # First signup and verify OTP
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    db.close()
    
    # Set username with invalid format
    response = client.post("/api/auth/set-username", 
                         json={"email": TEST_EMAIL, "username": "InvalidUsername"})
    assert response.status_code == 400
    assert "Username must be lowercase and alphanumeric" in response.json()["detail"]

def test_auth_set_username_already_taken(cleanup_test_data):
    """Test username setting with already taken username"""
    # First user
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    
    # Second user with same username
    second_email = "seconduser@example.com"
    client.post("/api/auth/signup", json={"email": second_email})
    second_otp_record = db.query(OTP).filter(OTP.email == second_email).first()
    assert second_otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": second_email, "otp": second_otp_record.otp})
    db.close()
    
    response = client.post("/api/auth/set-username", 
                         json={"email": second_email, "username": TEST_USERNAME})
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]

def test_auth_set_username_user_not_found():
    """Test username setting for non-existent user"""
    response = client.post("/api/auth/set-username", 
                         json={"email": "nonexistent@example.com", "username": TEST_USERNAME})
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_auth_login_success(cleanup_test_data):
    """Test successful login"""
    # Complete signup process
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    db.close()
    
    # Login
    response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_auth_login_user_not_found():
    """Test login for non-existent user"""
    response = client.post("/api/auth/login", json={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_auth_login_email_not_verified(cleanup_test_data):
    """Test login with unverified email"""
    # Signup but don't verify
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    
    response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    assert response.status_code == 400
    assert "Email not verified" in response.json()["detail"]

def test_auth_login_username_not_set(cleanup_test_data):
    """Test login without setting username"""
    # Signup and verify but don't set username
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    db.close()
    
    response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    assert response.status_code == 400
    assert "Username not set" in response.json()["detail"]

# Room API Tests
def test_rooms_create_room_success(cleanup_test_data):
    """Test successful room creation"""
    # Complete signup process
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    
    # Login to get token
    login_response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    token = login_response.json()["access_token"]
    db.close()
    
    # Create room
    response = client.post("/api/rooms/", 
                          json={"name": "Test Room", "description": "A test room"},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Room"
    assert response.json()["description"] == "A test room"

def test_rooms_list_rooms(cleanup_test_data):
    """Test listing rooms"""
    # Complete signup process
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    
    # Login to get token
    login_response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    token = login_response.json()["access_token"]
    db.close()
    
    # List rooms
    response = client.get("/api/rooms/", 
                         headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_rooms_get_room(cleanup_test_data):
    """Test getting room details"""
    # Complete signup process
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    
    # Login to get token
    login_response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    token = login_response.json()["access_token"]
    
    # Create room
    create_response = client.post("/api/rooms/", 
                                 json={"name": "Test Room", "description": "A test room"},
                                 headers={"Authorization": f"Bearer {token}"})
    room_id = create_response.json()["room_id"]
    db.close()
    
    # Get room details
    response = client.get(f"/api/rooms/{room_id}", 
                         headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["room_id"] == room_id

def test_rooms_join_room(cleanup_test_data):
    """Test joining a room"""
    # Complete signup process
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    
    # Login to get token
    login_response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    token = login_response.json()["access_token"]
    
    # Create room
    create_response = client.post("/api/rooms/", 
                                 json={"name": "Test Room", "description": "A test room"},
                                 headers={"Authorization": f"Bearer {token}"})
    room_id = create_response.json()["room_id"]
    db.close()
    
    # Join room
    response = client.post(f"/api/rooms/{room_id}/join", 
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_rooms_leave_room(cleanup_test_data):
    """Test leaving a room"""
    # Complete signup process
    client.post("/api/auth/signup", json={"email": TEST_EMAIL})
    db = SessionLocal()
    otp_record = db.query(OTP).filter(OTP.email == TEST_EMAIL).first()
    assert otp_record is not None
    client.post("/api/auth/verify-otp", 
               json={"email": TEST_EMAIL, "otp": otp_record.otp})
    client.post("/api/auth/set-username", 
               json={"email": TEST_EMAIL, "username": TEST_USERNAME})
    
    # Login to get token
    login_response = client.post("/api/auth/login", json={"email": TEST_EMAIL})
    token = login_response.json()["access_token"]
    
    # Create room
    create_response = client.post("/api/rooms/", 
                                 json={"name": "Test Room", "description": "A test room"},
                                 headers={"Authorization": f"Bearer {token}"})
    room_id = create_response.json()["room_id"]
    db.close()
    
    # Join room first
    client.post(f"/api/rooms/{room_id}/join", 
               headers={"Authorization": f"Bearer {token}"})
    
    # Leave room
    response = client.post(f"/api/rooms/{room_id}/leave", 
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

# Test the API root endpoint
def test_api_root_endpoint():
    """Test the API root endpoint"""
    response = client.get("/api/")
    assert response.status_code == 200
    assert "message" in response.json()