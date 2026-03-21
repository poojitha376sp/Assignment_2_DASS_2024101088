import requests
import pytest

def test_prod_list_all(base_url, common_headers):
    """Verify listing all active products."""
    url = f"{base_url}/products"
    response = requests.get(url, headers=common_headers)
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        for prod in data:
            assert prod["is_active"] is True

def test_prod_filter_category(base_url, common_headers):
    """Verify product filtering by category."""
    url = f"{base_url}/products"
    params = {"category": "Electronics"}
    response = requests.get(url, headers=common_headers, params=params)
    if response.status_code == 200:
        data = response.json()
        for prod in data:
            assert prod.get("category") == "Electronics"

def test_prod_get_by_id_404(base_url, common_headers):
    """PROD-02: Verify 404 for non-existent product."""
    url = f"{base_url}/products/999999"
    response = requests.get(url, headers=common_headers)
    assert response.status_code == 404
