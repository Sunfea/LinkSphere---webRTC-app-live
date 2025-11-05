#!/usr/bin/env python3
"""
Script to test rooms endpoint
"""

import requests
import json

def test_rooms_endpoint():
    """Test rooms endpoint"""
    # Use the token we generated earlier
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZXd1c2VyMTIzIiwiZXhwIjoxNzYyMjk3NzUxfQ.rkgXEWoDHCvTKl4q-naIvLusir-XzaIZNmvVgpe46zE"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Test GET /api/rooms/
    try:
        response = requests.get("http://localhost:8000/api/rooms/", headers=headers)
        print(f"GET /api/rooms/ - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error testing GET /api/rooms/: {e}")

if __name__ == "__main__":
    test_rooms_endpoint()