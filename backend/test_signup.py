import requests
import json

# Test the signup endpoint
url = "http://localhost:8000/api/auth/signup"
data = {"email": "test@example.com"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")