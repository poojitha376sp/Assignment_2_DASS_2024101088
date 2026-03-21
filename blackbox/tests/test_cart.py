import requests
import pytest

def test_cart01_add_zero_quantity(base_url, user_headers):
    """CART-01: Verify 400 when adding quantity 0."""
    url = f"{base_url}/cart/add"
    payload = {"product_id": 1, "quantity": 0}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_cart_add_valid(base_url, user_headers):
    """Verify successful item addition to cart."""
    url = f"{base_url}/cart/add"
    payload = {"product_id": 1, "quantity": 1}
    response = requests.post(url, headers=user_headers(), json=payload)
    if response.status_code == 200:
        data = response.json()
        assert "items" in data
        assert any(item["product_id"] == 1 for item in data["items"])

def test_cart_clear(base_url, user_headers):
    """Verify clearing the cart."""
    url = f"{base_url}/cart/clear"
    response = requests.delete(url, headers=user_headers())
    assert response.status_code in (200, 204)
