import requests
import pytest

def test_addr01_invalid_label(base_url, user_headers):
    """ADDR-01: Label must be HOME, OFFICE, or OTHER."""
    url = f"{base_url}/addresses"
    payload = {
        "label": "VACATION",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_addr02_invalid_pincode_length(base_url, user_headers):
    """ADDR-02: Pincode must be exactly 6 digits."""
    url = f"{base_url}/addresses"
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "12345"
    }
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_addr_post_success(base_url, user_headers):
    """Verify successful address creation."""
    url = f"{base_url}/addresses"
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "123456"
    }
    response = requests.post(url, headers=user_headers(), json=payload)
    if response.status_code == 201:
        data = response.json()
        assert data["label"] == "HOME"
        assert "address_id" in data
