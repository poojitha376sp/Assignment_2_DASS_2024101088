import requests
import pytest

def test_review_rating_range(base_url, user_headers):
    """Verify 400 for rating outside 1-5."""
    url = f"{base_url}/products/1/reviews"
    payload = {"rating": 6, "comment": "Invalid rating"}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_review_comment_length(base_url, user_headers):
    """Verify comment length constraint (1-200 chars)."""
    url = f"{base_url}/products/1/reviews"
    payload = {"rating": 5, "comment": ""}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_review_get_average(base_url, common_headers):
    """Verify average rating is a decimal."""
    url = f"{base_url}/products/1/reviews"
    response = requests.get(url, headers=common_headers)
    if response.status_code == 200:
        data = response.json()
        assert "average_rating" in data
        assert isinstance(data["average_rating"], float) or isinstance(data["average_rating"], int)
