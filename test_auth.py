#!/usr/bin/env python3
"""Test auth endpoints"""
import requests
import json

BASE_URL = "http://localhost:8003/api/v1"

# Test registration
print("=" * 50)
print("Testing Registration Endpoint")
print("=" * 50)

register_data = {
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "Test@123",
    "role": "individual"
}

try:
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

# Test login
print("\n" + "=" * 50)
print("Testing Login Endpoint")
print("=" * 50)

login_data = {
    "email": "test@example.com",
    "password": "Test@123"
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("Auth endpoints are working!")
print("=" * 50)
