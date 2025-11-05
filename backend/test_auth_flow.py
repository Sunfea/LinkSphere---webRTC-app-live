#!/usr/bin/env python3
"""
Script to test the complete authentication flow
"""

import requests
import json

def test_auth_flow():
    """Test the complete authentication flow"""
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error testing root endpoint: {e}")
        return
    
    # Test signup endpoint
    signup_data = {
        "email": "testflow@example.com"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/signup", json=signup_data)
        print(f"Signup: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error testing signup endpoint: {e}")
        return
    
    print("\n=== Authentication Flow Test Completed ===")
    print("Check the terminal output for the OTP that was generated.")
    print("Use that OTP to test the verify-otp endpoint.")

if __name__ == "__main__":
    test_auth_flow()