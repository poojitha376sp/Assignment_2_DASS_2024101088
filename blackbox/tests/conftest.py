import pytest

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL of the QuickCart API."""
    return "http://localhost:8080/api/v1"

@pytest.fixture(scope="session")
def roll_number():
    """Return the roll number for the X-Roll-Number header."""
    return 2024101088

@pytest.fixture(scope="session")
def common_headers(roll_number):
    """Return common headers used for most requests."""
    return {
        "X-Roll-Number": str(roll_number),
        "Content-Type": "application/json"
    }

@pytest.fixture
def user_headers(common_headers):
    """Fixture to provide headers for a specific user. Default: User ID 1."""
    def _headers(user_id=1):
        headers = common_headers.copy()
        headers["X-User-ID"] = str(user_id)
        return headers
    return _headers
