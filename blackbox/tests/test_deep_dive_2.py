import requests
import pytest

def test_wall03_max_topup_limit(base_url, user_headers):
    """WALL-03: Verify 400 when adding more than 100,000."""
    url = f"{base_url}/wallet/add"
    payload = {"amount": 100001}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_loy02_min_redeem_limit(base_url, user_headers):
    """LOY-02: Verify 400 when redeeming less than 1 point."""
    url = f"{base_url}/loyalty/redeem"
    payload = {"points": 0}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_supp03_invalid_open_to_closed(base_url, user_headers, common_headers):
    """SUPP-03: Verify OPEN cannot skip to CLOSED directly."""
    # 1. Get all tickets to find an OPEN one or create one
    url_list = f"{base_url}/admin/tickets" # Use admin to see all
    res = requests.get(url_list, headers=common_headers)
    tickets = res.json()
    open_ticket = next((t for t in tickets if t["status"] == "OPEN"), None)
    
    if open_ticket:
        t_id = open_ticket["ticket_id"]
        url_update = f"{base_url}/support/tickets/{t_id}"
        # Try OPEN -> CLOSED (Illegal)
        response = requests.put(url_update, headers=user_headers(user_id=open_ticket["user_id"]), json={"status": "CLOSED"})
        assert response.status_code == 400
