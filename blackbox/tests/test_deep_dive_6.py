import requests
import pytest

def test_supp05_unauthorized_update(base_url, user_headers, common_headers):
    """SUPP-05: Verify User A cannot update User B's ticket."""
    # 1. Get a ticket belonging to some user
    res = requests.get(f"{base_url}/admin/tickets", headers=common_headers)
    tickets = res.json()
    if tickets:
        target = tickets[0]
        t_id = target["ticket_id"]
        # 2. Try to update it as User 999 (Unauthorized)
        unauth_headers = user_headers(user_id=999) 
        if target["user_id"] == 999: unauth_headers = user_headers(user_id=888)
        
        response = requests.put(f"{base_url}/support/tickets/{t_id}", headers=unauth_headers, json={"status": "IN_PROGRESS"})
        assert response.status_code == 403, "Should return 403 Forbidden for cross-user update"

def test_coup04_reuse_limit(base_url, user_headers):
    """Verify if a coupon is one-time use per user."""
    url = f"{base_url}/coupon/apply"
    # 1. Use coupon once (Assume valid cart exists)
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": 1})
    requests.post(url, headers=user_headers(), json={"code": "SAVE10"})
    requests.post(f"{base_url}/checkout", headers=user_headers(), json={"payment_method": "WALLET"})
    
    # 2. Try using it again in a new order
    requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 2, "quantity": 1})
    response = requests.post(url, headers=user_headers(), json={"code": "SAVE10"})
    assert response.status_code == 400, "Should reject reused one-time coupon"

def test_review_avg_calculation(base_url, user_headers):
    """Verify average rating is calculated correctly (not just truncated)."""
    # 1. Place orders to allow reviews (Mocked/Pre-existing user 1 has orders usually)
    # 2. Add two reviews: 5 and 4
    url = f"{base_url}/reviews"
    requests.post(url, headers=user_headers(user_id=1), json={"product_id": 1, "rating": 5, "comment": "Great!"})
    requests.post(url, headers=user_headers(user_id=2), json={"product_id": 1, "rating": 4, "comment": "Good"})
    
    # 3. Check average
    params = {"product_id": 1}
    response = requests.get(f"{base_url}/reviews/average", headers=user_headers(), params=params)
    avg = response.json()["average_rating"]
    assert avg == 4.5, f"Expected 4.5, got {avg}"

def test_ord03_invoice_404(base_url, user_headers):
    """ORD-03: Verify 404 for non-existent order invoice."""
    url = f"{base_url}/orders/999999/invoice"
    response = requests.get(url, headers=user_headers())
    assert response.status_code == 404, "Should return 404 for missing order"
