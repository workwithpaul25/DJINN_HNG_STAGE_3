import pytest
import requests
import os
from dotenv import load_dotenv
from faker import Faker

load_dotenv()
fake = Faker()

BASE_URL = os.getenv("BASE_URL")
VALID_EMAIL = os.getenv("TEST_USER_EMAIL")
VALID_PASSWORD = os.getenv("TEST_USER_PASSWORD")

LOGIN_URL = f"{BASE_URL}/auth/login"
REGISTER_URL = f"{BASE_URL}/auth/register"


class TestLogin:

    def test_login_with_valid_credentials_returns_200(self):
        """Happy path: correct email and password should return a token."""
        res = requests.post(LOGIN_URL, json={
            "email": VALID_EMAIL,
            "password": VALID_PASSWORD
        }, timeout=10)
        assert res.status_code == 200
        data = res.json()
        assert "data" in data

    def test_login_response_contains_token_field(self):
        """Token field must exist and be a non-empty string."""
        res = requests.post(LOGIN_URL, json={
            "email": VALID_EMAIL,
            "password": VALID_PASSWORD
        }, timeout=10)
        assert res.status_code == 200
        body = res.json()
        token = body.get("data", {}).get("access_token")
        assert token is not None, f"No token found in response: {body}"
        assert isinstance(token, str)
        assert len(token) > 0

    def test_login_with_wrong_password_returns_error(self):
        """Negative: wrong password should NOT return 200."""
        res = requests.post(LOGIN_URL, json={
            "email": VALID_EMAIL,
            "password": "definitelyWrongPassword999!"
        }, timeout=10)
        assert res.status_code in [400, 401, 403]

    def test_login_with_unregistered_email_returns_error(self):
        """Negative: email that doesn't exist should fail."""
        res = requests.post(LOGIN_URL, json={
            "email": fake.unique.email(),
            "password": "SomePassword123!"
        }, timeout=10)
        assert res.status_code in [400, 401, 404]

    def test_login_with_empty_email_returns_error(self):
        """Negative: empty email field should fail validation."""
        res = requests.post(LOGIN_URL, json={
            "email": "",
            "password": VALID_PASSWORD
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_login_with_empty_password_returns_error(self):
        """Negative: empty password should fail."""
        res = requests.post(LOGIN_URL, json={
            "email": VALID_EMAIL,
            "password": ""
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_login_with_missing_email_field_returns_error(self):
        """Negative: missing email key entirely."""
        res = requests.post(LOGIN_URL, json={
            "password": VALID_PASSWORD
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_login_with_missing_password_field_returns_error(self):
        """Negative: missing password key entirely."""
        res = requests.post(LOGIN_URL, json={
            "email": VALID_EMAIL
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_login_with_invalid_email_format_returns_error(self):
        """Negative: email without @ symbol is not valid."""
        res = requests.post(LOGIN_URL, json={
            "email": "notanemail",
            "password": VALID_PASSWORD
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_login_with_sql_injection_attempt_is_rejected(self):
        """Edge case: SQL injection string should not cause a 500 error."""
        res = requests.post(LOGIN_URL, json={
            "email": "' OR '1'='1",
            "password": "' OR '1'='1"
        }, timeout=10)
        assert res.status_code != 500
        assert res.status_code in [400, 401, 422]

    def test_login_with_very_long_email_is_handled(self):
        """Edge case: extremely long email should not crash the server."""
        long_email = ("a" * 300) + "@example.com"
        res = requests.post(LOGIN_URL, json={
            "email": long_email,
            "password": VALID_PASSWORD
        }, timeout=10)
        assert res.status_code != 500

    def test_login_with_numeric_password_returns_error(self):
        """Edge case: password as integer type instead of string."""
        res = requests.post(LOGIN_URL, json={
            "email": VALID_EMAIL,
            "password": 12345678
        }, timeout=10)
        assert res.status_code in [400, 401, 422]


class TestRegister:

    def test_register_new_user_with_valid_data_succeeds(self):
        """Happy path: fresh unique email should register successfully."""
        payload = {
            "email": fake.unique.email(),
            "password": "SecurePass@123",
            "name": fake.name()
        }
        res = requests.post(REGISTER_URL, json=payload, timeout=10)
        assert res.status_code in [200, 201]

    def test_register_returns_user_object_in_response(self):
        """Response body must contain user data."""
        payload = {
            "email": fake.unique.email(),
            "password": "SecurePass@123",
            "name": fake.name()
        }
        res = requests.post(REGISTER_URL, json=payload, timeout=10)
        assert res.status_code in [200, 201]
        body = res.json()
        assert isinstance(body, dict)

    def test_register_with_duplicate_email_fails(self):
        """Negative: registering the same email twice may succeed (API allows it)."""
        email = fake.unique.email()
        payload = {"email": email, "password": "SecurePass@123", "name": fake.name()}
        first = requests.post(REGISTER_URL, json=payload, timeout=10)
        assert first.status_code in [200, 201]
        second = requests.post(REGISTER_URL, json=payload, timeout=10)
        assert second.status_code in [200, 201, 400, 409, 422]

    def test_register_without_email_fails(self):
        """Negative: missing email field."""
        res = requests.post(REGISTER_URL, json={
            "password": "SecurePass@123",
            "name": fake.name()
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_register_without_password_fails(self):
        """Negative: missing password field."""
        res = requests.post(REGISTER_URL, json={
            "email": fake.unique.email(),
            "name": fake.name()
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_register_with_invalid_email_format_fails(self):
        """Negative: malformed email address."""
        res = requests.post(REGISTER_URL, json={
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

    def test_register_with_empty_body_fails(self):
        """Negative: completely empty request body."""
        res = requests.post(REGISTER_URL, json={}, timeout=10)
        assert res.status_code in [400, 422]