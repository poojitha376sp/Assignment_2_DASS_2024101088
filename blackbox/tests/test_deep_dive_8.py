import requests
import pytest

def test_prod05_inactive_visibility(base_url, user_headers, common_headers):
    """PROD-05: Verify inactive products are hidden even in direct lookup."""
    # 1. As admin, find an active product and deactivate it
    res = requests.get(f"{base_url}/admin/products", headers=common_headers)
    products = res.json()
    if products:
        prod = products[0]
        p_id = prod["product_id"]
        # Deactivate (Spec: "Admin can update product details... including active state")
        requests.put(f"{base_url}/admin/products/{p_id}", headers=common_headers, json={"active": False})
        
        # 2. Try to fetch as user
        response = requests.get(f"{base_url}/products/{p_id}", headers=user_headers())
        assert response.status_code == 404, "Inactive product should return 404 to users"

def test_rev05_unordered_review(base_url, user_headers):
    """REV-05: Verify user cannot review a product they haven't ordered."""
    # User 99 has no orders
    url = f"{base_url}/reviews"
    response = requests.post(url, headers=user_headers(user_id=99), json={
        "product_id": 1,
        "rating": 5,
        "comment": "Nice!"
    })
    assert response.status_code == 400, "Should reject review for unordered product"

def test_rev06_duplicate_review(base_url, user_headers):
    """REV-06: Verify user cannot review the same product twice."""
    # 1. First review
    url = f"{base_url}/reviews"
    requests.post(url, headers=user_headers(user_id=1), json={"product_id": 1, "rating": 5, "comment": "A"})
    
    # 2. Second review
    response = requests.post(url, headers=user_headers(user_id=1), json={"product_id": 1, "rating": 4, "comment": "B"})
    assert response.status_code == 400, "Should reject duplicate review"

def test_coup05_percentage_boundary(base_url, common_headers):
    """COUP-05: Verify admin cannot create a >100% discount coupon."""
    url = f"{base_url}/admin/coupons"
    payload = {
        "code": "FREE_FOREVER",
        "discount_type": "PERCENTAGE",
        "discount_value": 110, # > 100%
        "min_cart_value": 0
    }
    response = requests.post(url, headers=common_headers, json=payload)
    assert response.status_code == 400, "Should reject percentage discount > 100%"
