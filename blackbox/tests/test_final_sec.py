import requests
import pytest

def test_sec_07_regular_user_admin_access(base_url, user_headers):
    """SEC-07: Verify regular user cannot access admin endpoints."""
    url = f"{base_url}/admin/users"
    # Sending X-User-ID: 1 (regular user) but NO admin flag (if one exists)
    # The X-Roll-Number is present.
    response = requests.get(url, headers=user_headers())
    # Should probably be 403 or 401. 
    # But wait, does the API use X-User-ID to determine admin status?
    # Some APIs use user_id < 100 as admin.
    assert response.status_code in [401, 403], f"Admin endpoint accessible to regular user! Status: {response.status_code}"

def test_sec_08_empty_headers(base_url):
    """SEC-08: Verify no headers at all results in rejection."""
    url = f"{base_url}/products"
    response = requests.get(url)
    assert response.status_code == 401, "Endpoint accessible without any headers!"
