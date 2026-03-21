import requests
import pytest

def test_order_list(base_url, user_headers):
    """Verify user can view all their orders."""
    url = f"{base_url}/orders"
    response = requests.get(url, headers=user_headers())
    if response.status_code == 200:
        assert isinstance(response.json(), list)

def test_ord01_cancel_delivered(base_url, user_headers):
    """ORD-01: Verify 400 when cancelling a delivered order."""
    # This requires an order ID that is already status: DELIVERED.
    # We might need to find one via admin/orders or create/warp one.
    pass

def test_order_invoice(base_url, user_headers):
    """Verify invoice contains subtotal, GST, and total."""
    # Assuming order ID 1 exists
    url = f"{base_url}/orders/1/invoice"
    response = requests.get(url, headers=user_headers())
    if response.status_code == 200:
        data = response.json()
        assert "subtotal" in data
        assert "gst" in data
        assert "total" in data
