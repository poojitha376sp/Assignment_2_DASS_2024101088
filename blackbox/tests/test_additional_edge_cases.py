import requests


def test_edge_cart_missing_product_id(base_url, user_headers):
    """Cart add should reject requests missing the product_id field."""
    response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"quantity": 1},
    )
    assert response.status_code == 400


def test_edge_cart_malformed_json(base_url, user_headers):
    """Cart add should reject malformed JSON payloads."""
    response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        data='{"product_id": 1, "quantity": }',
    )
    assert response.status_code == 400


def test_edge_cart_missing_content_type(base_url, user_headers):
    """Cart add should reject a body sent without JSON content type."""
    headers = user_headers()
    headers.pop("Content-Type", None)
    response = requests.post(
        f"{base_url}/cart/add",
        headers=headers,
        data='{"product_id": 1, "quantity": 1}',
    )
    assert response.status_code in (400, 415)


def test_edge_profile_phone_float(base_url, user_headers):
    """Profile update should reject a float phone number."""
    response = requests.put(
        f"{base_url}/profile",
        headers=user_headers(),
        json={"name": "Valid Name", "phone": 123.45},
    )
    assert response.status_code == 400


def test_edge_review_rating_float(base_url, user_headers):
    """Review creation should reject float ratings instead of integers."""
    response = requests.post(
        f"{base_url}/products/1/reviews",
        headers=user_headers(),
        json={"rating": 4.5, "comment": "Float rating"},
    )
    assert response.status_code == 400