Project Overview

This project contains a comprehensive automated test suite for the Zedu REST API. It tests authentication, user management, and protected endpoints with a focus on:

1. Happy path testing Valid inputs return expected results
2. Negative testing Invalid inputs are properly rejected
3. Edge case testing Boundary conditions and unusual inputs are handled gracefully

Total Tests: 37+ covering login, registration, token validation, password reset, and user profile endpoints.

---

Prerequisites

Before running this project, ensure you have:

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| pip | Latest |
| Git | Latest |

To check your versions:**
```bash
python --version
pip --version
git --version
```

---

## Setup Instructions ##

1. Clone the Repository

```bash
git clone https://github.com/workwithpaul25/DJINN_HNG_STAGE_3/
cd zedu-api-tests
```


2. Create and Activate Virtual Environment

On Windows:
```bash
python -m venv venv
venv\\Scripts\\activate
```

You'll know it worked when you see `(venv)` at the start of your terminal line.

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set Up Environment Variables

Copy the example file:
```bash
cp .env.example .env
```

Open `.env` and fill in your Zedu credentials:

> IMPORTANT: The `.env` file is listed in `.gitignore` and will NOT be pushed to GitHub. Keep your credentials safe!

---

## Running the Tests

Run All Tests
```bash
pytest tests/ -v
```

Run a Specific Test File
```bash
pytest tests/test_auth.py -v
```

Run a Specific Test
```bash
pytest tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200 -v
```

Generate an HTML Report
```bash
pytest tests/ -v --html=reports/report.html --self-contained-html
```

Then open `reports/report.html` in your browser.

---

Project Structure

---

## Test Coverage

### `tests/test_auth.py`
Tests for authentication endpoints:
- Login with valid/invalid credentials
- Registration with valid/invalid data
- Missing or empty fields
- Invalid email formats
- Edge cases

### `tests/test_users.py`
Tests for user endpoints:
- User registration
- Duplicate email handling
- User profile retrieval
- Email field validation

### `tests/test_password_reset.py`
Tests for password/auth endpoints:
- Password reset requests
- Magic link generation
- Email verification
- Token validation

---

## Key Features

1. No Hardcoded Credentials All secrets are in `.env` only

2. Single Login Function `utils/auth.py` is the only place login logic exists

3. Independent Tests Every test can run alone

4. Idempotent Tests use `faker` to generate unique data

5. Comprehensive Assertions Each test validates status codes, fields, data types, and values

6. Session-Scoped Token Login happens once per test run

---

## Requirements

All dependencies are listed in `requirements.txt` with pinned versions:

---

Happy Testing!

