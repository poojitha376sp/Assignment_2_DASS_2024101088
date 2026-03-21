import requests
import pytest

def test_inventory_recovery_on_cancel(base_url, user_headers, common_headers):
    """Verify stock is recovered when an order is cancelled."""
    # 1. Get initial stock using admin endpoint
    res_prof = requests.get(f"{base_url}/admin/products", headers=common_headers)
    data = res_prof.json()
    prod = next(p for p in data if p.get("product_id") == 1)
    initial_stock = prod.get("stock", 0)
    
    # 2. Add to cart and checkout
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    res_check = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "WALLET"})
    order_id = res_check.json().get("order_id")
    
    if order_id:
        # 3. Cancel order
        requests.post(f"{base_url}/orders/{order_id}/cancel", headers=user_headers())
        
        # 4. Verify stock restored
        res_prod_final = requests.get(f"{base_url}/admin/products", headers=common_headers)
        prod_final = next(p for p in res_prod_final.json() if p.get("product_id") == 1)
        assert prod_final.get("stock") == initial_stock, f"Stock mismatch: {prod_final.get('stock')} != {initial_stock}"

def test_coupon_max_discount_cap(base_url, user_headers, common_headers):
    """Verify coupon discount does not exceed the cap."""
    res_coups = requests.get(f"{base_url}/admin/coupons", headers=common_headers)
    data = res_coups.json()
    coupon = next((c for c in data if c.get("max_discount")), None)
    
    if coupon:
        code = coupon.get("code") or coupon.get("coupon_code")
        cap = coupon["max_discount"]
        
        # Setup cart with high value
        requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 10})
        
        # Apply coupon
        res_apply = requests.post(f"{base_url}/coupon/apply", headers=user_headers(), json={"code": code})
        applied_discount = res_apply.json().get("discount_amount", 0)
        assert applied_discount <= cap, f"Discount {applied_discount} exceeds cap {cap}"

def test_gst_calculation_precision(base_url, user_headers):
    """Verify GST is exactly 5%."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    
    # Get cart total
    res_cart = requests.get(f"{base_url}/cart", headers=user_headers())
    subtotal = res_cart.json().get("total", 0)
    
    # Checkout
    res_check = requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "WALLET"})
    order_id = res_check.json().get("order_id")
    
    if order_id:
        res_inv = requests.get(f"{base_url}/orders/{order_id}/invoice", headers=user_headers())
        invoice = res_inv.json()
        expected_gst = subtotal * 0.05
        # Verify 5% GST
        assert abs(invoice.get("gst", 0) - expected_gst) < 0.01
