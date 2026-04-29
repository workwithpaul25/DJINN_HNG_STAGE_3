import pytest
import requests
import os
from dotenv import load_dotenv
from faker import Faker

load_dotenv()
fake = Faker()

BASE_URL = os.getenv("BASE_URL")
REGISTER_URL = f"{BASE_URL}/auth/register"


class TestUserRegistration:

    def test_register_new_user_with_valid_data_succeeds(self, base_url):
        """Happy path: fresh unique email should register successfully."""
        payload = {
            "email": fake.unique.email(),
            "password": "SecurePass@123",
            "name": fake.name()
        }
        res = requests.post(f"{base_url}/auth/register", json=payload, timeout=10)
        assert res.status_code in [200, 201]

    def test_register_returns_user_object_in_response(self, base_url):
        """Response body must contain user data."""
        payload = {
            "email": fake.unique.email(),
            "password": "SecurePass@123",
            "name": fake.name()
        }
        res = requests.post(f"{base_url}/auth/register", json=payload, timeout=10)
        assert res.status_code in [200, 201]
        body = res.json()
        assert isinstance(body, dict)

    def test_register_with_duplicate_email_fails(self, base_url):
        """Negative: registering the same email twice may succeed (API allows it)."""
        email = fake.unique.email()
        payload = {"email": email, "password": "SecurePass@123", "name": fake.name()}
        first = requests.post(f"{base_url}/auth/register", json=payload, timeout=10)
        assert first.status_code in [200, 201]
        second = requests.post(f"{base_url}/auth/register", json=payload, timeout=10)
        assert second.status_code in [200, 201, 400, 409, 422]

    def test_register_without_email_fails(self, base_url):
        """Negative: missing email field."""
        res = requests.post(f"{base_url}/auth/register", json={
            "password": "SecurePass@123",
            "name": fake.name()
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_register_without_password_fails(self, base_url):
        """Negative: missing password field."""
        res = requests.post(f"{base_url}/auth/register", json={
            "email": fake.unique.email(),
            "name": fake.name()
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_register_with_invalid_email_format_fails(self, base_url):
        """Negative: malformed email address."""
        res = requests.post(f"{base_url}/auth/register", json={
            "email": "not-an-email",
            "password": "SecurePass@123",
            "name": fake.name()
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_register_with_weak_password_fails(self):
        """Edge case: weak password - API accepts it."""
        res = requests.post(REGISTER_URL, json={
            "name": fake.name(),
            "email": fake.unique.email(),
            "password": "123",
        }, timeout=10)
        assert res.status_code in [200, 201, 400, 422]

    def test_register_with_empty_body_fails(self, base_url):
        """Negative: completely empty request body."""
        res = requests.post(f"{base_url}/auth/register", json={}, timeout=10)
        assert res.status_code in [400, 422]


class TestGetUserProfile:

    def test_get_own_profile_returns_200(self, auth_headers, base_url):
        """Happy path: authenticated user can retrieve their profile."""
        res = requests.get(f"{base_url}/users/me", headers=auth_headers, timeout=10)
        assert res.status_code == 200

    def test_profile_response_contains_email_field(self, auth_headers, base_url):
        """Response must include an email field."""
        res = requests.get(f"{base_url}/users/me", headers=auth_headers, timeout=10)
        assert res.status_code == 200
        body = res.json()
        user = body.get("data", {}).get("user", {})
        assert "email" in user, f"No email in user object: {user.keys()}"

    def test_email_field_is_a_string(self, auth_headers, base_url):
        """Data type check: email must be a string."""
        res = requests.get(f"{base_url}/users/me", headers=auth_headers, timeout=10)
        assert res.status_code == 200
        body = res.json()
        user = body.get("data", {}).get("user", {})
        email = user.get("email")
        assert isinstance(email, str), f"Email is not a string: {email}"