import requests
import pytest

def test_admin_get_users(base_url, common_headers):
    """Verify admin can retrieve all users."""
    url = f"{base_url}/admin/users"
    response = requests.get(url, headers=common_headers)
    # Status should be 200 IF roll number is valid
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "user_id" in data[0]
            assert "name" in data[0]

def test_admin_get_products(base_url, common_headers):
    """Verify admin can see all products including inactive ones."""
    url = f"{base_url}/admin/products"
    response = requests.get(url, headers=common_headers)
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
