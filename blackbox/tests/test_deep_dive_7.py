import requests
import pytest

def test_sec_leak_audit(base_url):
    """Audit all main endpoints for missing X-Roll-Number leak."""
    endpoints = [
        ("/products", "GET"),
        ("/products/1", "GET"),
        ("/profile", "GET"),
        ("/addresses", "GET"),
        ("/cart", "GET"),
        ("/admin/users", "GET"),
        ("/admin/products", "GET"),
        ("/admin/coupons", "GET"),
        ("/admin/tickets", "GET")
    ]
    
    leaked = []
    for ep, method in endpoints:
        url = f"{base_url}{ep}"
        # Hit without X-Roll-Number
        res = requests.request(method, url)
        if res.status_code != 401:
            leaked.append(ep)
            
    assert not leaked, f"Security Leak! Endpoints working without X-Roll-Number: {leaked}"

def test_user_id_leak_audit(base_url, common_headers):
    """Audit user-scoped endpoints for missing X-User-ID leak."""
    endpoints = [
        ("/profile", "GET"),
        ("/addresses", "GET"),
        ("/cart", "GET"),
        ("/checkout", "POST"),
        ("/wallet/balance", "GET"),
        ("/orders", "GET")
    ]
    
    leaked = []
    for ep, method in endpoints:
        url = f"{base_url}{ep}"
        # Hit with X-Roll-Number but NO X-User-ID
        res = requests.request(method, url, headers=common_headers)
        if res.status_code != 400: # Docs say 400 for missing user-id
            leaked.append(ep)
            
    assert not leaked, f"Security Leak! Endpoints working without X-User-ID: {leaked}"

def test_order_financial_math(base_url, user_headers):
    """Verify subtotal + gst == total calculation."""
    # 1. Setup cart
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    res_cart = requests.get(f"{base_url}/cart", headers=user_headers())
    cart_total = res_cart.json().get("total", 0)
    
    # 2. Checkout
    res_check = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "WALLET"})
    order_id = res_check.json().get("order_id")
    
    if order_id:
        res_inv = requests.get(f"{base_url}/orders/{order_id}/invoice", headers=user_headers())
        invoice = res_inv.json()
        
        subtotal = invoice.get("subtotal", 0)
        gst = invoice.get("gst", 0)
        total = invoice.get("total", 0)
        
        # Verify simple math
        assert abs((subtotal + gst) - total) < 0.01, f"Math error: {subtotal} + {gst} != {total}"
        # Verify cart match
        assert subtotal == cart_total, f"Subtotal {subtotal} should match cart total {cart_total}"
