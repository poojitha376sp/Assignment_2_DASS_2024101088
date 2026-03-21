import requests
import pytest

def test_sec01_missing_roll_header(base_url):
    """SEC-01: Verify 401 when X-Roll-Number is missing."""
    url = f"{base_url}/admin/users"
    response = requests.get(url)
    assert response.status_code == 401

def test_sec02_invalid_roll_type(base_url):
    """SEC-02: Verify 400 when X-Roll-Number is not an integer."""
    url = f"{base_url}/admin/users"
    headers = {"X-Roll-Number": "ABC"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 400

def test_sec03_missing_user_header(base_url, common_headers):
    """SEC-03: Verify 400 when X-User-ID is missing on scoped endpoint."""
    url = f"{base_url}/profile"
    response = requests.get(url, headers=common_headers)
    assert response.status_code == 400
