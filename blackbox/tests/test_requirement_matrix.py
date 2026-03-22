from datetime import datetime, timezone
from math import ceil

import requests


def test_admin_inspection_endpoints_return_lists(base_url, common_headers):
    """Verify the admin inspection endpoints return list responses."""
    endpoints = [
        "/admin/users",
        "/admin/orders",
        "/admin/carts",
        "/admin/addresses",
        "/admin/coupons",
        "/admin/tickets",
    ]

    for endpoint in endpoints:
        response = requests.get(f"{base_url}{endpoint}", headers=common_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_cart_update_and_remove_round_trip(base_url, user_headers):
    """Verify cart update and remove both mutate cart state correctly."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())

    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 1},
    )
    assert add_response.status_code == 200

    update_response = requests.post(
        f"{base_url}/cart/update",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 2},
    )
    assert update_response.status_code == 200

    cart_response = requests.get(f"{base_url}/cart", headers=user_headers())
    assert cart_response.status_code == 200
    cart = cart_response.json()
    assert any(item.get("product_id") == 1 and item.get("quantity") == 2 for item in cart.get("items", []))

    remove_response = requests.post(
        f"{base_url}/cart/remove",
        headers=user_headers(),
        json={"product_id": 1},
    )
    assert remove_response.status_code == 200

    final_cart = requests.get(f"{base_url}/cart", headers=user_headers()).json()
    assert final_cart.get("items", []) == []
    assert final_cart.get("total", 0) == 0


def test_cart_update_rejects_excessive_quantity(base_url, user_headers):
    """Verify cart updates cannot exceed available stock."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 1},
    )
    assert add_response.status_code == 200

    update_response = requests.post(
        f"{base_url}/cart/update",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 1000000},
    )
    assert update_response.status_code == 400


def test_cart_update_rejects_missing_product(base_url, user_headers):
    """Verify cart updates reject nonexistent products."""
    update_response = requests.post(
        f"{base_url}/cart/update",
        headers=user_headers(),
        json={"product_id": 99999999, "quantity": 1},
    )
    assert update_response.status_code == 404


def test_cart_update_requires_product_id(base_url, user_headers):
    """Verify cart updates require product_id in the request body."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 1},
    )
    update_response = requests.post(
        f"{base_url}/cart/update",
        headers=user_headers(),
        json={"quantity": 1},
    )
    assert update_response.status_code == 400


def test_cart_total_matches_item_sum(base_url, user_headers):
    """Verify cart total matches the sum of item subtotals."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 1},
    )
    assert add_response.status_code == 200

    cart = requests.get(f"{base_url}/cart", headers=user_headers()).json()
    item_sum = sum(item.get("subtotal", 0) for item in cart.get("items", []))
    assert cart.get("total") == item_sum
    assert cart.get("total") == 120


def test_cart_add_quantity_two_has_correct_subtotal(base_url, user_headers):
    """Verify adding quantity 2 computes the correct line-item subtotal."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 2},
    )
    assert add_response.status_code == 200

    cart = requests.get(f"{base_url}/cart", headers=user_headers()).json()
    item = cart.get("items", [])[0]
    assert item.get("quantity") == 2
    assert item.get("subtotal") == 240


def test_coupon_remove_round_trip(base_url, user_headers, common_headers):
    """Verify an applied coupon can be removed again."""
    coupons_response = requests.get(f"{base_url}/admin/coupons", headers=common_headers)
    coupons = coupons_response.json()
    coupon = next(
        (
            entry
            for entry in coupons
            if entry.get("coupon_code") and entry.get("is_active")
            and entry.get("expiry_date")
            and datetime.fromisoformat(entry["expiry_date"].replace("Z", "+00:00")) > datetime.now(timezone.utc)
        ),
        None,
    )
    assert coupon is not None

    products_response = requests.get(f"{base_url}/products", headers=user_headers())
    products = products_response.json()
    product = next(entry for entry in products if entry.get("product_id") == 1)
    unit_price = product["price"]
    min_cart_value = coupon.get("min_cart_value", 0)
    quantity = max(1, ceil(min_cart_value / unit_price))

    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": quantity},
    )
    assert add_response.status_code == 200

    apply_response = requests.post(
        f"{base_url}/coupon/apply",
        headers=user_headers(),
        json={"code": coupon["coupon_code"]},
    )
    assert apply_response.status_code == 200

    remove_response = requests.post(
        f"{base_url}/coupon/remove",
        headers=user_headers(),
        json={"code": coupon["coupon_code"]},
    )
    assert remove_response.status_code == 200
    assert remove_response.json().get("message") == "Coupon removed successfully"


def test_order_cancel_nonexistent_returns_404(base_url, user_headers):
    """Verify cancelling a missing order returns 404."""
    response = requests.post(f"{base_url}/orders/99999999/cancel", headers=user_headers())
    assert response.status_code == 404


def test_order_cancel_delivered_returns_400(base_url, user_headers):
    """Verify delivered orders cannot be cancelled."""
    admin_headers = {"X-Roll-Number": "2024101088", "Content-Type": "application/json"}
    orders_response = requests.get(f"{base_url}/admin/orders", headers=admin_headers)
    orders = orders_response.json()
    delivered = next(
        (
            order
            for order in orders
            if order.get("order_status") == "DELIVERED" or order.get("status") == "DELIVERED"
        ),
        None,
    )
    assert delivered is not None

    order_id = delivered.get("order_id") or delivered.get("id")
    response = requests.post(f"{base_url}/orders/{order_id}/cancel", headers=user_headers())
    assert response.status_code == 400


def test_review_comment_upper_bound_rejected(base_url, user_headers):
    """Verify comments longer than 200 characters are rejected."""
    response = requests.post(
        f"{base_url}/products/1/reviews",
        headers=user_headers(),
        json={"rating": 5, "comment": "A" * 201},
    )
    assert response.status_code == 400


def test_review_average_zero_for_unreviewed_product(base_url, user_headers):
    """Verify a product with no reviews reports an average rating of 0."""
    response = requests.get(f"{base_url}/products/14/reviews", headers=user_headers())
    assert response.status_code == 200
    data = response.json()
    assert data.get("average_rating") == 0
    assert data.get("reviews") == []


def test_support_ticket_creation_keeps_message_and_open_status(base_url, user_headers):
    """Verify support tickets preserve the message text and start OPEN."""
    payload = {
        "subject": "Need help with checkout",
        "message": "This message should be stored exactly as written.",
    }
    response = requests.post(f"{base_url}/support/ticket", headers=user_headers(), json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data.get("message") == payload["message"]
    assert data.get("status") == "OPEN"
    assert data.get("subject") == payload["subject"]


def test_support_ticket_cannot_reopen_closed_ticket(base_url, user_headers):
    """Verify a closed support ticket cannot be reopened."""
    create_response = requests.post(
        f"{base_url}/support/ticket",
        headers=user_headers(),
        json={"subject": "Transition probe", "message": "Testing state flow"},
    )
    assert create_response.status_code == 200
    ticket_id = create_response.json()["ticket_id"]

    close_response = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers(),
        json={"status": "IN_PROGRESS"},
    )
    assert close_response.status_code == 200
    close_response = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers(),
        json={"status": "CLOSED"},
    )
    assert close_response.status_code == 200

    reopen_response = requests.put(
        f"{base_url}/support/tickets/{ticket_id}",
        headers=user_headers(),
        json={"status": "OPEN"},
    )
    assert reopen_response.status_code == 400


def test_address_update_rejects_forbidden_fields(base_url, user_headers):
    """Verify address updates cannot change label, city, or pincode."""
    response = requests.get(f"{base_url}/addresses", headers=user_headers())
    assert response.status_code == 200
    addresses = response.json()
    assert addresses

    address_id = addresses[0].get("address_id") or addresses[0].get("id")
    for payload in [{"city": "New City"}, {"pincode": "999999"}, {"label": "OFFICE"}]:
        update_response = requests.put(
            f"{base_url}/addresses/{address_id}",
            headers=user_headers(),
            json=payload,
        )
        assert update_response.status_code == 400


def test_coupon_remove_invalid_code_rejected(base_url, user_headers):
    """Verify removing an invalid coupon code is rejected."""
    response = requests.post(
        f"{base_url}/coupon/remove",
        headers=user_headers(),
        json={"code": "INVALID_CODE"},
    )
    assert response.status_code == 400


def test_wallet_add_and_pay_exact_balance_change(base_url, user_headers):
    """Verify wallet add and pay adjust balance by the exact requested amounts."""
    before = requests.get(f"{base_url}/wallet", headers=user_headers()).json()["wallet_balance"]

    add_response = requests.post(
        f"{base_url}/wallet/add",
        headers=user_headers(),
        json={"amount": 50},
    )
    assert add_response.status_code == 200

    after_top_up = requests.get(f"{base_url}/wallet", headers=user_headers()).json()["wallet_balance"]
    assert abs(after_top_up - (before + 50)) < 0.0001

    pay_response = requests.post(
        f"{base_url}/wallet/pay",
        headers=user_headers(),
        json={"amount": 10},
    )
    assert pay_response.status_code == 200

    after_pay = requests.get(f"{base_url}/wallet", headers=user_headers()).json()["wallet_balance"]
    assert abs(after_pay - (after_top_up - 10)) < 0.0001


def test_wallet_add_boundary_values(base_url, user_headers):
    """Verify wallet top-up respects the documented upper bound."""
    valid = requests.post(
        f"{base_url}/wallet/add",
        headers=user_headers(),
        json={"amount": 100000},
    )
    assert valid.status_code == 200

    invalid = requests.post(
        f"{base_url}/wallet/add",
        headers=user_headers(),
        json={"amount": 100000.01},
    )
    assert invalid.status_code == 400


def test_new_default_address_clears_old_defaults(base_url, user_headers):
    """Verify creating a new default address leaves exactly one default address."""
    addresses = requests.get(f"{base_url}/addresses", headers=user_headers()).json()
    for address in addresses:
        requests.put(
            f"{base_url}/addresses/{address['address_id']}",
            headers=user_headers(),
            json={"street": address["street"], "is_default": False},
        )

    create_response = requests.post(
        f"{base_url}/addresses",
        headers=user_headers(),
        json={
            "label": "HOME",
            "street": "99999 Regression Lane",
            "city": "Pune",
            "pincode": "544658",
            "is_default": True,
        },
    )
    assert create_response.status_code == 200
    new_address_id = create_response.json()["address"]["address_id"]

    refreshed = requests.get(f"{base_url}/addresses", headers=user_headers()).json()
    default_ids = [address["address_id"] for address in refreshed if address.get("is_default")]
    assert default_ids == [new_address_id]


def test_invoice_total_matches_checkout_total(base_url, user_headers):
    """Verify invoice total matches the actual checkout total exactly."""
    requests.delete(f"{base_url}/cart/clear", headers=user_headers())
    add_response = requests.post(
        f"{base_url}/cart/add",
        headers=user_headers(),
        json={"product_id": 1, "quantity": 2},
    )
    assert add_response.status_code == 200

    cart = requests.get(f"{base_url}/cart", headers=user_headers()).json()
    checkout_response = requests.post(
        f"{base_url}/checkout",
        headers=user_headers(),
        json={"payment_method": "WALLET"},
    )
    assert checkout_response.status_code == 200
    order_id = checkout_response.json()["order_id"]

    invoice_response = requests.get(f"{base_url}/orders/{order_id}/invoice", headers=user_headers())
    assert invoice_response.status_code == 200
    invoice = invoice_response.json()
    assert abs(invoice["total_amount"] - checkout_response.json()["total_amount"]) < 0.01
    assert abs(invoice["subtotal"] + invoice["gst_amount"] - invoice["total_amount"]) < 0.01


def test_review_average_keeps_decimal_precision(base_url, user_headers):
    """Verify review averages keep decimal precision instead of rounding down."""
    product_id = None
    for candidate in range(1, 300):
        response = requests.get(f"{base_url}/products/{candidate}/reviews", headers=user_headers())
        if response.status_code == 200:
            data = response.json()
            if data.get("average_rating") == 0 and not data.get("reviews"):
                product_id = candidate
                break

    assert product_id is not None
    requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers=user_headers(),
        json={"rating": 5, "comment": "Decimal average A"},
    )
    requests.post(
        f"{base_url}/products/{product_id}/reviews",
        headers={**user_headers(user_id=2)},
        json={"rating": 4, "comment": "Decimal average B"},
    )

    response = requests.get(f"{base_url}/products/{product_id}/reviews", headers=user_headers())
    assert response.status_code == 200
    data = response.json()
    assert data["average_rating"] == 4.5