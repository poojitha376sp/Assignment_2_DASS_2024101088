import requests
import pytest

def test_chck03_empty_cart(base_url, user_headers):
    """CHCK-03: Verify 400 when checking out with an empty cart."""
    # 1. Clear cart
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    
    # 2. Checkout
    url = f"{base_url}/checkout"
    response = requests.post(url, headers=user_headers(), json={"payment_method": "WALLET"})
    assert response.status_code == 400, "Should reject checkout for empty cart"

def test_ord02_double_cancel(base_url, user_headers):
    """ORD-02: Verify 400 when cancelling an already cancelled order."""
    # 1. Create order
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    res_check = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "WALLET"})
    order_id = res_check.json().get("order_id")
    
    if order_id:
        # 2. First cancellation
        requests.post(f"{base_url}/orders/{order_id}/cancel", headers=user_headers())
        
        # 3. Second cancellation
        response = requests.post(f"{base_url}/orders/{order_id}/cancel", headers=user_headers())
        assert response.status_code == 400, "Should reject second cancellation"

def test_wall04_extreme_negative(base_url, user_headers):
    """WALL-04: Verify 400 for negative wallet top-up."""
    url = f"{base_url}/wallet/add"
    response = requests.post(url, headers=user_headers(), json={"amount": -1000000})
    assert response.status_code == 400

def test_addr05_put_invalid_pincode(base_url, user_headers):
    """ADDR-05: Verify 400 when updating address with invalid pincode."""
    # 1. Get an existing address ID
    res = requests.get(f"{base_url}/addresses", headers=user_headers())
    addrs = res.json()
    if addrs:
        addr_id = addrs[0].get("address_id") or addrs[0].get("id")
        url = f"{base_url}/addresses/{addr_id}"
        payload = {"pincode": "ABCDEF"} # Non-digits
        response = requests.put(url, headers=user_headers(), json=payload)
        assert response.status_code == 400
