import requests
import pytest

def test_wall01_insufficient_balance(base_url, user_headers):
    """WALL-01: Verify 400 when paying more than balance."""
    url = f"{base_url}/wallet/pay"
    payload = {"amount": 9999999}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_wall02_invalid_topup_amount(base_url, user_headers):
    """WALL-02: Verify 400 for negative top-up amount."""
    url = f"{base_url}/wallet/add"
    payload = {"amount": -10}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_loy01_insufficient_points(base_url, user_headers):
    """LOY-01: Verify 400 when redeeming more points than owned."""
    url = f"{base_url}/loyalty/redeem"
    payload = {"points": 999999}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400
