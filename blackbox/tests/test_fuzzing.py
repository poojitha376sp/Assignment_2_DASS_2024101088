import requests
import pytest
import random

def test_fuzz_product_search(base_url, user_headers):
    """Fuzz product search with special characters."""
    fuzz_strings = ["'", "!", "*", "%", "--", ";", "../../etc/passwd", "OR 1=1", "<script>"]
    for s in fuzz_strings:
        response = requests.get(f"{base_url}/products", headers=user_headers(), params={"search": s})
        # Should either return a list (maybe empty) or 400. Should NOT 500.
        assert response.status_code in [200, 400], f"Search crashed with {s}"

def test_fuzz_cart_quantities(base_url, user_headers):
    """Fuzz cart quantities with large and weird numbers."""
    fuzz_values = [999999999999, -999999999999, 0.5, "ten", None, "1e6"]
    for v in fuzz_values:
        response = requests.post(f"{base_url}/cart/add", headers=user_headers(), json={"product_id": 1, "quantity": v})
        # Should be 400 for invalid types/bounds
        assert response.status_code == 400, f"Cart accepted weird quantity: {v}"

def test_fuzz_profile_fields(base_url, user_headers):
    """Fuzz profile update with various types."""
    fuzz_values = [
        {"name": "A" * 1000, "phone": "1234567890"}, # Too long
        {"name": "Tester", "phone": "00000000000"}, # Too many digits
        {"name": 123, "phone": "1234567890"}, # Int instead of string
        {"name": "Tester", "phone": [1,2,3]} # List instead of string
    ]
    for p in fuzz_values:
        response = requests.put(f"{base_url}/profile", headers=user_headers(), json=p)
        assert response.status_code == 400, f"Profile accepted invalid data: {p}"

def test_fuzz_address_pincode_types(base_url, user_headers):
    """Fuzz pincode with different types."""
    fuzz_values = [123456, 12345.6, "123 45", True, None]
    for v in fuzz_values:
        response = requests.post(f"{base_url}/addresses", headers=user_headers(), json={
            "label": "HOME", "street": "S", "city": "C", "pincode": v
        })
        assert response.status_code == 400, f"Address accepted invalid pincode: {v}"
