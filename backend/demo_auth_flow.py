#!/usr/bin/env python3
"""
Demo script to demonstrate the full authentication flow:
1. Register with email and password
2. Verify OTP (sent to console)
3. Login with username and password
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

def register_user(email, password):
    """Register a new user"""
    url = f"{BASE_URL}{API_PREFIX}/auth/register"
    data = {
        "email": email,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Register response: {response.status_code}")
        print(f"Register data: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error during registration: {e}")
        return None

def verify_otp(email, otp):
    """Verify OTP"""
    url = f"{BASE_URL}{API_PREFIX}/auth/verify-otp"
    data = {
        "email": email,
        "otp": otp
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Verify OTP response: {response.status_code}")
        print(f"Verify OTP data: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"Error during OTP verification: {e}")
        return None

def login_user(username, password):
    """Login with username and password"""
    url = f"{BASE_URL}{API_PREFIX}/auth/login"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Login response: {response.status_code}")
        if response.status_code == 200:
            print(f"Login successful!")
            print(f"Token: {response.json().get('access_token')}")
            return response.json()
        else:
            print(f"Login failed: {response.json()}")
            return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None

def main():
    # Test data
    email = "demo@example.com"
    password = "demo123"
    
    print("=== WebRTC Authentication Flow Demo ===\n")
    
    # Step 1: Register
    print("Step 1: Register")
    register_result = register_user(email, password)
    if not register_result:
        print("Registration failed!")
        return
    
    # Step 2: Verify OTP
    print("\nStep 2: Verify OTP")
    print("Check the console output for the OTP code that was 'sent' to your email.")
    otp = input("Enter the OTP code from the console: ")
    verify_result = verify_otp(email, otp)
    if not verify_result:
        print("OTP verification failed!")
        return
    
    # Extract username from verification result
    message = verify_result.get("message", "")
    # The message should contain something like "Your username is: testuser"
    import re
    username_match = re.search(r"Your username is: (\w+)", message)
    if username_match:
        username = username_match.group(1)
        print(f"Extracted username: {username}")
    else:
        username = input("Enter your username (from the console output): ")
    
    # Step 3: Login
    print("\nStep 3: Login")
    login_result = login_user(username, password)
    if not login_result:
        print("Login failed!")
        return
    
    print("\n=== Authentication Flow Completed Successfully! ===")

if __name__ == "__main__":
    main()