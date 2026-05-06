# DJINN HNG Stage 3 — Zedu API Test Suite

[![CI — Run Test Suite](https://github.com/workwithpaul25/DJINN_HNG_STAGE_3/actions/workflows/ci.yml/badge.svg)](https://github.com/workwithpaul25/DJINN_HNG_STAGE_3/actions/workflows/ci.yml)

> Comprehensive automated test suite for the Zedu REST API, built with Python and pytest.

---

## Project Overview

Tests cover authentication, user management, and protected endpoints across three areas:

1. **Happy path testing** — Valid inputs return expected results
2. **Negative testing** — Invalid inputs are properly rejected
3. **Edge case testing** — Boundary conditions and unusual inputs are handled gracefully

**Total Tests: 37+** covering login, registration, token validation, password reset, and user profile endpoints.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.11+   |
| pip         | Latest  |
| Git         | Latest  |

```bash
python --version
pip --version
git --version
```

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/workwithpaul25/DJINN_HNG_STAGE_3.git
cd DJINN_HNG_STAGE_3
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root (never commit this file):

```bash
cp .env.example .env   # if the example file exists
# OR create it manually:
```

```env
BASE_URL=https://your-zedu-api-base-url.com
USER_EMAIL=your_test_account@example.com
USER_PASSWORD=your_test_password
```

> `.env` is listed in `.gitignore` and will NOT be pushed to GitHub. Keep your credentials safe.

---

## Running Tests Locally

```bash
# Run the full suite (verbose)
pytest api_automation/ -v

# Run a specific test file
pytest api_automation/tests/test_auth.py -v

# Run a specific test
pytest api_automation/tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200 -v

# Generate JUnit XML report (mirrors what CI produces)
pytest api_automation/ -v --junitxml=reports/junit-report.xml

# Generate HTML report
pytest api_automation/ -v --html=reports/html-report.html --self-contained-html
```

---

## Environment Variables

| Variable        | Description                          | Required |
|-----------------|--------------------------------------|----------|
| `BASE_URL`      | Root URL of the Zedu API             | ✅ Yes   |
| `USER_EMAIL`    | Email address of the test account    | ✅ Yes   |
| `USER_PASSWORD` | Password of the test account         | ✅ Yes   |

In **local** development these are loaded from `.env` via `python-dotenv`.  
In **CI** (GitHub Actions) they are injected as repository secrets — see the *CI Pipeline* section below.

---

## CI Pipeline

The pipeline is defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) and uses **GitHub Actions**.

### How it works

| Step | What happens |
|------|-------------|
| **Trigger** | Runs automatically on every `push` and `pull_request` to any branch |
| **Environment** | Ubuntu latest runner, Python 3.11 |
| **Install** | `pip install -r requirements.txt` — all pinned versions |
| **Run tests** | `pytest api_automation/ -v --tb=short --junitxml=reports/junit-report.xml --html=reports/html-report.html` |
| **Fail fast** | pytest exits with a non-zero code if any test fails — the job fails immediately |
| **Upload** | Test reports (JUnit XML + HTML) are uploaded as artifacts for every run, pass or fail |

### Adding secrets to GitHub

Go to **Settings → Secrets and variables → Actions → New repository secret** and add:

- `BASE_URL`
- `USER_EMAIL`
- `USER_PASSWORD`

Without these, tests that hit the real API will fail at the authentication step — which is the correct and expected behaviour.

---

## Project Structure

```
DJINN_HNG_STAGE_3/
├── .github/
│   └── workflows/
│       └── ci.yml          # ← CI/CD pipeline definition
├── api_automation/
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── test_password_reset.py
│   └── utils/
│       └── auth.py
├── reports/                # generated at runtime, gitignored
├── requirements.txt
├── .env.example
└── README.md
```

---

## Test Coverage

### `tests/test_auth.py`
- Login with valid/invalid credentials
- Registration with valid/invalid data
- Missing or empty fields
- Invalid email formats
- Edge cases

### `tests/test_users.py`
- User registration
- Duplicate email handling
- User profile retrieval
- Email field validation

### `tests/test_password_reset.py`
- Password reset requests
- Magic link generation
- Email verification
- Token validation

---

## Key Design Decisions

| Principle | Implementation |
|-----------|---------------|
| No hardcoded credentials | All secrets live in `.env` / GitHub Secrets only |
| Single login function | `utils/auth.py` is the sole place login logic lives |
| Independent tests | Every test can run in isolation |
| Idempotent tests | `faker` generates unique data per run |
| Comprehensive assertions | Each test validates status codes, fields, types, and values |
| Session-scoped token | Login happens once per test run (performance) |

---

Happy Testing! 🚀
