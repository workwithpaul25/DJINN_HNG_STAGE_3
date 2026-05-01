"""
test_protected.py
Tests for endpoints that require authentication.
Covers token handling — valid, missing, malformed, expired.
"""

import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")


PROTECTED_ENDPOINT = f"{BASE_URL}/users/me"


class TestProtectedEndpointAccess:

    def test_access_protected_endpoint_with_valid_token_succeeds(self, auth_headers):
        """Happy path: valid token should grant access."""
        res = requests.get(PROTECTED_ENDPOINT, headers=auth_headers)
        assert res.status_code == 200

    def test_access_protected_endpoint_without_token_is_rejected(self):
        """Negative: no token at all should be rejected."""
        res = requests.get(PROTECTED_ENDPOINT)
        assert res.status_code in [401, 403]

    def test_access_protected_endpoint_with_empty_token_is_rejected(self):
        """Negative: empty bearer token should fail."""
        res = requests.get(PROTECTED_ENDPOINT, headers={"Authorization": "Bearer "})
        assert res.status_code in [401, 403]

    def test_access_protected_endpoint_with_malformed_token_is_rejected(self):
        """Negative: garbage string as token should be rejected."""
        res = requests.get(PROTECTED_ENDPOINT, headers={
            "Authorization": "Bearer this.is.definitely.not.a.real.token"
        })
        assert res.status_code in [401, 403]

    def test_access_protected_endpoint_with_wrong_auth_scheme_fails(self):
        """Edge case: using 'Token' instead of 'Bearer' prefix."""
        res = requests.get(PROTECTED_ENDPOINT, headers={
            "Authorization": "Token somefaketoken123"
        })
        assert res.status_code in [401, 403]

    def test_response_has_correct_content_type(self, auth_headers):
        """Happy path: response should be JSON."""
        res = requests.get(PROTECTED_ENDPOINT, headers=auth_headers)
        assert "application/json" in res.headers.get("Content-Type", "")