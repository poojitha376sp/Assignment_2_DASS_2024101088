import requests
import pytest

def test_addr04_pincode_alphanumeric(base_url, user_headers):
    """Verify 400 when pincode contains non-digits."""
    url = f"{base_url}/addresses"
    payload = {
        "label": "HOME",
        "street": "123 Street",
        "city": "City",
        "pincode": "123A56", # Non-digits
        "is_default": False
    }
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400, "Should reject non-digit pincode"

def test_coup03_double_application(base_url, user_headers):
    """Verify multiple coupons cannot be used together."""
    # 1. Apply first coupon
    url = f"{base_url}/coupon/apply"
    requests.post(url, headers=user_headers(), json={"code": "SAVE10"})
    
    # 2. Try applying second coupon
    response = requests.post(url, headers=user_headers(), json={"code": "OFF20"})
    assert response.status_code == 400, "Should reject second coupon application"

def test_supp04_closed_ticket_immutable(base_url, user_headers, common_headers):
    """Verify CLOSED tickets cannot be updated back to OPEN."""
    res = requests.get(f"{base_url}/admin/tickets", headers=common_headers)
    closed_ticket = next((t for t in res.json() if t["status"] == "CLOSED"), None)
    
    if closed_ticket:
        t_id = closed_ticket["ticket_id"]
        url = f"{base_url}/support/tickets/{t_id}"
        # Try CLOSED -> OPEN (Illegal)
        response = requests.put(url, headers=user_headers(user_id=closed_ticket["user_id"]), json={"status": "OPEN"})
        assert response.status_code == 400
