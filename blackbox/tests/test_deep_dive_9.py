import requests
import pytest
import time

def test_inv_05_recovery_on_cancel(base_url, common_headers, user_headers):
    """INV-05: Verify inventory is recovered when an order is cancelled."""
    # 1. Get initial stock
    res_init = requests.get(f"{base_url}/products/1", headers=user_headers())
    stock_before = res_init.json().get("stock", 0)
    
    # 2. Add to cart and checkout
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 5})
    res_check = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "COD"})
    o_id = res_check.json().get("order_id")
    
    # 3. Cancel order
    requests.post(f"{base_url}/orders/{o_id}/cancel", headers=user_headers())
    
    # 4. Check stock again
    res_after = requests.get(f"{base_url}/products/1", headers=user_headers())
    stock_after = res_after.json().get("stock", 0)
    
    assert stock_after == stock_before, f"Inventory was not recovered! {stock_before} -> {stock_after}"

def test_coup_06_reuse_after_cancel(base_url, user_headers):
    """COUP-06: Verify one-time coupon can be reused if the order was cancelled."""
    # Assuming SAVE10 is a one-time coupon
    code = "SAVE10"
    # 1. First order with coupon
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    requests.post(f"{base_url}/coupon/apply", headers=user_headers(), json={"code": code})
    res_check = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "COD"})
    o_id = res_check.json().get("order_id")
    
    # 2. Cancel it
    requests.post(f"{base_url}/orders/{o_id}/cancel", headers=user_headers())
    
    # 3. New cart, try coupon again
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    res_apply = requests.post(f"{base_url}/coupon/apply", headers=user_headers(), json={"code": code})
    
    assert res_apply.status_code == 200, "One-time coupon should be reusable if previous order was cancelled"

def test_admin_05_negative_price(base_url, common_headers):
    """ADMIN-05: Verify admin cannot set a negative product price."""
    url = f"{base_url}/admin/products/1"
    response = requests.put(url, headers=common_headers, json={"price": -100})
    assert response.status_code == 400, "Should reject negative prices"

def test_admin_06_negative_stock(base_url, common_headers):
    """ADMIN-06: Verify admin cannot set negative stock."""
    url = f"{base_url}/admin/products/1"
    response = requests.put(url, headers=common_headers, json={"stock": -10})
    assert response.status_code == 400, "Should reject negative stock"

def test_chck_04_double_click(base_url, user_headers):
    """CHCK-04: Verify race condition on double checkout."""
    # Add items
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    
    # Send two checkout requests simultaneously (sequential here but close)
    res1 = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "COD"})
    res2 = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "COD"})
    
    # Second should fail (empty cart)
    assert res2.status_code == 400, "Double checkout allowed! (Duplicate order)"
