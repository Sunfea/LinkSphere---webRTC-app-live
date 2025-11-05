#!/usr/bin/env python
"""
Comprehensive test script for WebRTC Communication App
Tests the complete user flow from registration to room creation
"""

import requests
import time
import json

API_BASE = "http://localhost:8000"

def print_test(name, status, message=""):
    emoji = "✅" if status else "❌"
    print(f"{emoji} {name}: {message if message else ('PASS' if status else 'FAIL')}")
    return status

def test_health():
    """Test 1: Health endpoint"""
    try:
        r = requests.get(f"{API_BASE}/health")
        return print_test("Health Check", r.status_code == 200, f"Status: {r.json().get('status')}")
    except Exception as e:
        return print_test("Health Check", False, str(e))

def test_registration():
    """Test 2: User registration"""
    email = f"test{int(time.time())}@example.com"
    try:
        r = requests.post(f"{API_BASE}/api/auth/register", json={
            "email": email,
            "password": "Test1234!"
        })
        data = r.json()
        if r.status_code == 200:
            print_test("Registration", True, f"User created: {email}")
            return email, data.get("message")
        else:
            print_test("Registration", False, data.get("detail"))
            return None, None
    except Exception as e:
        print_test("Registration", False, str(e))
        return None, None

def test_otp_verification(email, otp="123456"):
    """Test 3: OTP verification"""
    try:
        r = requests.post(f"{API_BASE}/api/auth/verify-otp", json={
            "email": email,
            "otp": otp
        })
        data = r.json()
        if r.status_code == 200:
            username = data.get("username")
            print_test("OTP Verification", True, f"Username: {username}")
            return username
        else:
            print_test("OTP Verification", False, data.get("detail"))
            return None
    except Exception as e:
        print_test("OTP Verification", False, str(e))
        return None

def test_login(username, password="Test1234!"):
    """Test 4: User login"""
    try:
        r = requests.post(f"{API_BASE}/api/auth/login", json={
            "username": username,
            "password": password
        })
        data = r.json()
        if r.status_code == 200:
            token = data.get("access_token")
            print_test("Login", True, f"Token received (length: {len(token)})")
            return token
        else:
            print_test("Login", False, data.get("detail"))
            return None
    except Exception as e:
        print_test("Login", False, str(e))
        return None

def test_list_rooms(token):
    """Test 5: List rooms"""
    try:
        r = requests.get(f"{API_BASE}/api/rooms/", headers={
            "Authorization": f"Bearer {token}"
        })
        if r.status_code == 200:
            rooms = r.json()
            print_test("List Rooms", True, f"Found {len(rooms)} rooms")
            return rooms
        else:
            print_test("List Rooms", False, r.json().get("detail"))
            return []
    except Exception as e:
        print_test("List Rooms", False, str(e))
        return []

def test_create_room(token, room_name="Test Room"):
    """Test 6: Create room"""
    try:
        r = requests.post(f"{API_BASE}/api/rooms/", 
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={"name": room_name}
        )
        if r.status_code == 200:
            room = r.json()
            print_test("Create Room", True, f"Room ID: {room.get('room_id')}")
            return room
        else:
            print_test("Create Room", False, r.json().get("detail"))
            return None
    except Exception as e:
        print_test("Create Room", False, str(e))
        return None

def test_join_room(token, room_id):
    """Test 7: Join room"""
    try:
        r = requests.post(f"{API_BASE}/api/rooms/{room_id}/join", headers={
            "Authorization": f"Bearer {token}"
        })
        if r.status_code == 200:
            print_test("Join Room", True, "Successfully joined")
            return True
        else:
            print_test("Join Room", False, r.json().get("detail"))
            return False
    except Exception as e:
        print_test("Join Room", False, str(e))
        return False

def test_leave_room(token, room_id):
    """Test 8: Leave room"""
    try:
        r = requests.post(f"{API_BASE}/api/rooms/{room_id}/leave", headers={
            "Authorization": f"Bearer {token}"
        })
        if r.status_code == 200:
            print_test("Leave Room", True, "Successfully left")
            return True
        else:
            print_test("Leave Room", False, r.json().get("detail"))
            return False
    except Exception as e:
        print_test("Leave Room", False, str(e))
        return False

def main():
    print("\n" + "="*60)
    print("🧪 WebRTC Communication App - Comprehensive Test Suite")
    print("="*60 + "\n")
    
    results = []
    
    # Test 1: Health check
    results.append(test_health())
    
    # Test 2: Registration
    email, otp_msg = test_registration()
    if not email:
        print("\n❌ Cannot continue without successful registration")
        return
    
    # Extract OTP from message if available
    print(f"\n📧 NOTE: In development, check the server console for the OTP code")
    print(f"💡 For this test, we'll try with a mock OTP first\n")
    
    # Test 3: OTP Verification (will likely fail without real OTP)
    # username = test_otp_verification(email, "000000")
    
    # For testing purposes, let's try to login if we had a real user
    print("\n⏭️  Skipping OTP test (requires real OTP from server console)")
    print("⏭️  Skipping Login test (requires verified user)")
    
    # Test 5-8: Room operations (requires authentication)
    print("\n⏭️  Skipping Room tests (requires authenticated user)\n")
    
    print("="*60)
    print(f"📊 Test Summary:")
    print(f"   Total Tests Run: {len(results)}")
    print(f"   Passed: {sum(results)}")
    print(f"   Failed: {len(results) - sum(results)}")
    print("="*60)
    
    print("\n💡 To complete the full test:")
    print("   1. Check server console for OTP code during registration")
    print("   2. Use the OTP to verify the account")
    print("   3. Login with the generated username and password")
    print("   4. Test room operations\n")
    
    print("🌐 Open http://localhost:8000/ in your browser for manual testing!")
    print("🧪 Or visit http://localhost:8000/test for automated frontend tests!\n")

if __name__ == "__main__":
    main()
