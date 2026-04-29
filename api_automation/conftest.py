import pytest
import requests
import os
from dotenv import load_dotenv
from faker import Faker
from utils.auth import get_auth_headers, get_auth_token

load_dotenv()

fake = Faker()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def auth_headers():
    """Provides authenticated headers for all tests that need them."""
    return get_auth_headers()

@pytest.fixture(scope="session")
def auth_token():
    """Provides the raw token."""
    return get_auth_token()

@pytest.fixture
def fake_user():
    """Generates a fresh fake user for each test."""
    return {
        "email": fake.unique.email(),
        "password": "Test@1234!",
        "name": fake.name(),
        "username": fake.unique.user_name()
    }