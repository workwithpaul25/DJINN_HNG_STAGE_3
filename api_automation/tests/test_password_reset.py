import os
import pytest
import requests
from faker import Faker
from dotenv import load_dotenv

load_dotenv()

fake = Faker()

BASE_URL      = os.getenv("BASE_URL")
VALID_EMAIL   = os.getenv("TEST_USER_EMAIL")

PASSWORD_RESET_URL        = f"{BASE_URL}/auth/password-reset"
PASSWORD_RESET_VERIFY_URL = f"{BASE_URL}/auth/password-reset/verify"
MAGICK_LINK_URL           = f"{BASE_URL}/auth/magick-link"
MAGICK_LINK_VERIFY_URL    = f"{BASE_URL}/auth/magick-link/verify"
CHANGE_PASSWORD_URL       = f"{BASE_URL}/auth/change-password"


class TestPasswordReset:

    def test_password_reset_request_with_valid_email_succeeds(self):
        """Happy path: valid registered email triggers a reset link."""
        res = requests.post(PASSWORD_RESET_URL, json={
            "email": VALID_EMAIL,
        }, timeout=10)
        assert res.status_code in [200, 202], (
            f"Got {res.status_code}. Body: {res.text}"
        )

    def test_password_reset_response_is_json(self):
        """Response must be a JSON object."""
        res = requests.post(PASSWORD_RESET_URL, json={
            "email": VALID_EMAIL,
        }, timeout=10)
        assert res.status_code in [200, 202]
        assert isinstance(res.json(), dict)

    def test_password_reset_with_empty_body_is_rejected(self):
        """Negative: empty body must fail."""
        res = requests.post(PASSWORD_RESET_URL, json={}, timeout=10)
        assert res.status_code in [400, 422]

    def test_password_reset_with_invalid_email_format_is_rejected(self):
        """Negative: email without @ must fail."""
        res = requests.post(PASSWORD_RESET_URL, json={
            "email": "notavalidemail",
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_password_reset_with_empty_email_string_is_rejected(self):
        """Negative: empty string as email must fail."""
        res = requests.post(PASSWORD_RESET_URL, json={
            "email": "",
        }, timeout=10)
        assert res.status_code in [400, 422]

    def test_password_reset_with_very_long_email_does_not_crash_server(self):
        """Edge case: 300-character email must not cause 500."""
        long_email = ("a" * 290) + "@test.com"
        res = requests.post(PASSWORD_RESET_URL, json={
            "email": long_email,
        }, timeout=10)
        assert res.status_code != 500


class TestPasswordResetVerify:

    def test_password_reset_verify_with_fake_token_is_rejected(self):
        """Negative: made-up reset token must be rejected."""
        res = requests.post(PASSWORD_RESET_VERIFY_URL, json={
            "token": "thisisacompletelyfaketoken12345",
            "password": "NewPassword@123!",
        }, timeout=10)
        assert res.status_code in [400, 401, 404, 422]

    def test_password_reset_verify_with_empty_body_is_rejected(self):
        """Negative: empty body must fail."""
        res = requests.post(PASSWORD_RESET_VERIFY_URL, json={}, timeout=10)
        assert res.status_code in [400, 422]


class TestMagickLink:

    def test_magick_link_request_with_valid_email_succeeds(self):
        """Happy path: valid email should trigger a magic link."""
        res = requests.post(MAGICK_LINK_URL, json={
            "email": VALID_EMAIL,
        }, timeout=10)
        assert res.status_code in [200, 202], (
            f"Got {res.status_code}. Body: {res.text}"
        )

    def test_magick_link_with_missing_email_is_rejected(self):
        """Negative: empty body must fail."""
        res = requests.post(MAGICK_LINK_URL, json={}, timeout=10)
        assert res.status_code in [400, 422]

    def test_magick_link_verify_with_fake_token_is_rejected(self):
        """Negative: made-up magic link token must be rejected."""
        res = requests.post(MAGICK_LINK_VERIFY_URL, json={
            "token": "totallyfakemagictoken99999",
        }, timeout=10)
        assert res.status_code in [400, 401, 404, 422]


class TestChangePassword:

    def test_change_password_without_token_is_rejected(self):
        """Negative: no token must return 401 or 403."""
        res = requests.put(CHANGE_PASSWORD_URL, json={
            "password": "NewPassword@123!",
            "token": "faketoken123"
        }, timeout=10)
        assert res.status_code in [401, 403]

    def test_change_password_with_fake_token_is_rejected(self):
        """Negative: made-up token must be rejected."""
        res = requests.put(CHANGE_PASSWORD_URL, headers={
            "Authorization": "Bearer faketoken.abc.xyz"
        }, json={
            "password": "NewPassword@123!",
            "token": "faketoken123"
        }, timeout=10)
        assert res.status_code in [400, 401, 422]

    def test_change_password_with_empty_body_is_rejected(self):
        """Negative: empty body must fail."""
        res = requests.put(CHANGE_PASSWORD_URL, json={}, timeout=10)
        assert res.status_code in [400, 401, 422]

    def test_change_password_with_missing_password_field_is_rejected(self):
        """Negative: missing new password field must fail."""
        res = requests.put(CHANGE_PASSWORD_URL, json={
            "token": "sometokenvalue"
        }, timeout=10)
        assert res.status_code in [400, 401, 422]

    def test_change_password_with_very_short_password_is_rejected(self):
        """Edge case: 2-character password must fail validation."""
        res = requests.put(CHANGE_PASSWORD_URL, json={
            "password": "ab",
            "token": "faketoken123"
        }, timeout=10)
        assert res.status_code in [400, 401, 422]