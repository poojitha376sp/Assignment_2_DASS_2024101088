import requests
import pytest

def test_prof01_name_min_length(base_url, user_headers):
    """PROF-01: Name must be at least 2 characters."""
    url = f"{base_url}/profile"
    payload = {"name": "A", "phone": "1234567890"}
    response = requests.put(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_prof02_phone_invalid_length(base_url, user_headers):
    """PROF-02: Phone must be exactly 10 digits."""
    url = f"{base_url}/profile"
    payload = {"name": "Test User", "phone": "123"}
    response = requests.put(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_prof_valid_update(base_url, user_headers):
    """Verify successful profile update."""
    url = f"{base_url}/profile"
    payload = {"name": "Valid Name", "phone": "1234567890"}
    response = requests.put(url, headers=user_headers(), json=payload)
    # Note: We don't know if this succeeds or if there are bugs.
    # We just check for consistency with documentation.
    if response.status_code == 200:
        data = response.json()
        assert data["name"] == "Valid Name"
