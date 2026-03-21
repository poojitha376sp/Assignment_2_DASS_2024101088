import requests
import pytest

# 1. PARAMETRIZED DATA GENERATORS
INVALID_TYPES = [123, 12.5, True, None, ["list"], {"dict": "val"}]
SPECIAL_CHARS = ["'", "\"", ";", "--", "<script>", "*", "?", "%"]
OVERFLOW_STR = "A" * 2000

# 1.1 Address Pincode Fuzzing (15+ cases)
@pytest.mark.parametrize("pincode", ["12345", "1234567", "123A56", "      ", "12 345"] + INVALID_TYPES)
def test_mass_addr_pincode(base_url, user_headers, pincode):
    """Verify pincode validation across all invalid types/lengths."""
    url = f"{base_url}/addresses"
    payload = {"label": "HOME", "street": "S", "city": "C", "pincode": pincode}
    res = requests.post(url, headers=user_headers(), json=payload)
    assert res.status_code == 400

# 1.2 Profile Phone Fuzzing (15+ cases)
@pytest.mark.parametrize("phone", ["123456789", "12345678901", "ABCDEFGHIJ", "!@#$%^&*()"] + INVALID_TYPES)
def test_mass_prof_phone(base_url, user_headers, phone):
    """Verify phone validation across all invalid types/lengths."""
    url = f"{base_url}/profile"
    payload = {"name": "Tester", "phone": phone}
    res = requests.put(url, headers=user_headers(), json=payload)
    assert res.status_code == 400

# 1.3 Support Ticket Subject Fuzzing (15+ cases)
@pytest.mark.parametrize("subject", ["Hi", " ", "A"*4, OVERFLOW_STR] + SPECIAL_CHARS)
def test_mass_supp_subject(base_url, user_headers, subject):
    """Verify support ticket subject constraints."""
    url = f"{base_url}/support/ticket"
    payload = {"subject": subject, "description": "Needs help with checkout issue."}
    res = requests.post(url, headers=user_headers(), json=payload)
    # 400 expected for <5 chars or overflow
    if len(str(subject)) < 5 or len(str(subject)) > 500:
        assert res.status_code == 400

# 1.4 Product Search Fuzzing (20+ cases)
@pytest.mark.parametrize("q", SPECIAL_CHARS + ["OR 1=1", "UNION SELECT", "admin'--", "%%", "%%%%"])
def test_mass_prod_search(base_url, user_headers, q):
    """Verify robust search parameter handling."""
    url = f"{base_url}/products"
    res = requests.get(url, headers=user_headers(), params={"search": q})
    # Search should handle special chars gracefully (200 empty or 400 rejection, NO 500)
    assert res.status_code in [200, 400]

# 1.5 Cart Quantity Fuzzing (20+ cases)
@pytest.mark.parametrize("qty", [0, -1, -999999, 0.5, 999999999, "none", "10", "   "] + INVALID_TYPES)
def test_mass_cart_qty(base_url, user_headers, qty):
    """Verify quantity validation for cart operations."""
    url = f"{base_url}/cart/add"
    res = requests.post(url, headers=user_headers(), json={"product_id": 1, "quantity": qty})
    assert res.status_code == 400

# 1.6 Review Rating Fuzzing (15+ cases)
@pytest.mark.parametrize("rating", [0, 6, -1, 1.5, "five", None, "   "] + SPECIAL_CHARS)
def test_mass_rev_rating(base_url, user_headers, rating):
    """Verify rating constraints (1-5)."""
    url = f"{base_url}/reviews"
    res = requests.post(url, headers=user_headers(), json={"product_id": 1, "rating": rating, "comment": "X"})
    assert res.status_code == 400

# 1.7 Wallet Amount Fuzzing (15+ cases)
@pytest.mark.parametrize("amt", [0, -1, 0.0001, 100000.01, "max", "   "] + INVALID_TYPES)
def test_mass_wallet_amt(base_url, user_headers, amt):
    """Verify wallet top-up constraints."""
    url = f"{base_url}/wallet/add"
    res = requests.post(url, headers=user_headers(), json={"amount": amt})
    assert res.status_code == 400

# 1.8 Combined Combinations (Multi-category Search)
@pytest.mark.parametrize("cat", ["ELECTRONICS", "Electronics", "electronics", "FOOD", "Food", "food", "NON_EXIST"])
@pytest.mark.parametrize("sort", ["price_asc", "price_desc", "invalid"])
def test_mass_prod_matrix(base_url, user_headers, cat, sort):
    """Verify search matrix across categories and sorting."""
    url = f"{base_url}/products"
    res = requests.get(url, headers=user_headers(), params={"category": cat, "sort": sort})
    assert res.status_code in [200, 400]
