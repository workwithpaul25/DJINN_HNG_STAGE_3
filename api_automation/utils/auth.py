import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
EMAIL = os.getenv("TEST_USER_EMAIL")
PASSWORD = os.getenv("TEST_USER_PASSWORD")


def get_auth_token() -> str:
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
    }
    response = requests.post(url, json=payload, timeout=10)
    assert response.status_code == 200, (
        f"Login failed!\nStatus: {response.status_code}\nBody: {response.text}"
    )
    data = response.json()
    # Token is at data.access_token
    token = data.get("data", {}).get("access_token")
    assert token, f"No token found in login response!\nFull response: {data}"
    return token


def get_auth_headers() -> dict:
    token = get_auth_token()
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }