import requests
import pytest

def test_addr03_only_one_default(base_url, user_headers):
    """ADDR-03: Verify only one address can be default at a time."""
    # 1. Add first address as default
    url = f"{base_url}/addresses"
    payload1 = {"label": "HOME", "street": "Street 1", "city": "City", "pincode": "123456", "is_default": True}
    res1 = requests.post(url, headers=user_headers(), json=payload1)
    addr1_id = res1.json()["address_id"]

    # 2. Add second address as default
    payload2 = {"label": "OFFICE", "street": "Street 2", "city": "City", "pincode": "654321", "is_default": True}
    res2 = requests.post(url, headers=user_headers(), json=payload2)
    
    # 3. Check first address status
    res3 = requests.get(url, headers=user_headers())
    addresses = res3.json()
    addr1 = next(a for a in addresses if a["address_id"] == addr1_id)
    assert addr1["is_default"] is False, "First address should no longer be default"

def test_prod_sorting_price_asc(base_url, user_headers):
    """Verify products are correctly sorted by price ASC."""
    url = f"{base_url}/products"
    params = {"sort": "price_asc"}
    response = requests.get(url, headers=user_headers(), params=params)
    data = response.json()
    assert isinstance(data, list), f"Expected list, got {data}"
    prices = [p["price"] for p in data]
    assert prices == sorted(prices), f"Prices not sorted: {prices}"

def test_cart_quantity_merge(base_url, user_headers):
    """Verify adding the same product twice merges quantities."""
    # 1. Clear cart
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    
    # 2. Add product once
    url = f"{base_url}/cart/add"
    requests.post(url, headers=user_headers(), json={"product_id": 1, "quantity": 1})
    
    # 3. Add same product again
    requests.post(url, headers=user_headers(), json={"product_id": 1, "quantity": 2})
    
    # 4. Check cart
    res = requests.get(f"{base_url}/cart", headers=user_headers())
    items = res.json()["items"]
    item = next(i for i in items if i["product_id"] == 1)
    assert item["quantity"] == 3, "Quantities should merge to 3"
