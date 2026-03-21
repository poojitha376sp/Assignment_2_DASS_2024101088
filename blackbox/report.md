# QuickCart Black-Box API Testing Report

This report documents the test case design, execution results, and bug reports for the QuickCart REST API.

---

## 1. Test Case Design

### 1.1 Header & Security Validation
Every request must include `X-Roll-Number`. User-scoped endpoints also require `X-User-ID`.

| ID | Endpoint | Method | Input (Headers/Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | `/api/v1/admin/users` | GET | Missing `X-Roll-Number` | `401 Unauthorized` | Verify mandatory system access control. |
| **SEC-02** | `/api/v1/admin/users` | GET | `X-Roll-Number`: "ABC" | `400 Bad Request` | Verify data type validation for headers (integer required). |
| **SEC-03** | `/api/v1/profile` | GET | Missing `X-User-ID` | `400 Bad Request` | Verify user scoping for personal data. |
| **SEC-04** | `/api/v1/profile` | GET | `X-User-ID`: -5 | `400 Bad Request` | Verify boundary validation (must be positive integer). |
| **SEC-05** | `/api/v1/support/tickets/{id}`| PUT | User A updates User B ticket| `403 Forbidden` | Verify multi-user access control and data privacy. |

### 1.2 Profile & Address Management
Validating constraints on user-submitted data.

| ID | Endpoint | Method | Input (Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PROF-01** | `/api/v1/profile` | PUT | `{"name": "A", "phone": "1234567890"}` | `400 Bad Request` | Verify name length constraint (min 2 chars). |
| **PROF-02** | `/api/v1/profile` | PUT | `{"name": "Tester", "phone": "123"}` | `400 Bad Request` | Verify phone length constraint (exactly 10 digits). |
| **ADDR-01** | `/api/v1/addresses` | POST | `{"label": "VACATION", ...}` | `400 Bad Request` | Verify enum constraint (HOME, OFFICE, OTHER only). |
| **ADDR-02** | `/api/v1/addresses` | POST | `{"pincode": "1234567"}` | `400 Bad Request` | Verify pincode length constraint (exactly 6 digits). |
| **ADDR-03** | `/api/v1/addresses` | POST | Adding 2nd default address | Existing default is unset | Verify "only one default address" business logic. |
| **ADDR-04** | `/api/v1/addresses` | POST | `{"pincode": "123A56"}` | `400 Bad Request` | Verify data type validation (digits only) on CREATE. |
| **ADDR-05** | `/api/v1/addresses/{id}`| PUT | `{"pincode": "ABCDEF"}` | `400 Bad Request` | Verify data type validation (digits only) on UPDATE. |

### 1.3 Product Catalog
Testing search, filter, and visibility rules.

| ID | Endpoint | Method | Input (Query) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PROD-01** | `/api/v1/products` | GET | None | List of active products only | Verify privacy/state filtering (inactive products hidden). |
| **PROD-02** | `/api/v1/products/9999` | GET | ID: 9999 (Non-existent) | `404 Not Found` | Verify error handling for missing resources. |
| **PROD-03** | `/api/v1/products` | GET | `sort=price_asc` | Sorted JSON list | Verify sorting logic and numerical accuracy. |
| **PROD-04** | `/api/v1/products` | GET | `category=...&search=...` | Combined filter results | Verify multi-parameter query processing. |

### 1.4 Cart & Checkout Logic
Verifying transaction rules and financial correctness.

| ID | Endpoint | Method | Input (Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CART-01** | `/api/v1/cart/add` | POST | `{"product_id": 1, "quantity": 0}` | `400 Bad Request` | Verify minimum quantity constraint. |
| **CART-02** | `/api/v1/cart/add` | POST | `{"product_id": 1, "quantity": 1000}` | `400 Bad Request` | Verify inventory/stock check logic. |
| **CART-03** | `/api/v1/cart/add` | POST | Add same item twice | Merged quantities | Verify quantity accumulation (not replacement). |
| **COUP-01** | `/api/v1/coupon/apply` | POST | `{"code": "SAVE10"}` (Low Cart Value) | `400 Bad Request` | Verify minimum cart value constraint for coupons. |
| **COUP-02** | `/api/v1/coupon/apply` | POST | Large cart value | Cap applied | Verify maximum discount cap enforcement. |
| **CHCK-01** | `/api/v1/checkout` | POST | `{"payment_method": "BITCOIN"}` | `400 Bad Request` | Verify restricted payment methods (COD, WALLET, CARD only). |
| **CHCK-02** | `/api/v1/checkout` | POST | `{"payment_method": "COD"}` (Order > 5000) | `400 Bad Request` | Verify COD upper limit constraint ($5000). |
| **FIN-01** | `/api/v1/checkout` | POST | Valid Cart | `GST: 5%` calculation | Verify tax calculation accuracy and precision. |

### 1.5 Wallet & Loyalty Points
Testing balance management and point redemption.

| ID | Endpoint | Method | Input (Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WALL-01** | `/api/v1/wallet/pay` | POST | `{"amount": 999999}` | `400 Bad Request` | Verify insufficient balance handling. |
| **WALL-02** | `/api/v1/wallet/add` | POST | `{"amount": -10}` | `400 Bad Request` | Verify positive amount constraint for top-ups. |
| **LOY-01** | `/api/v1/loyalty/redeem`| POST | `{"points": 1}` (Zero balance) | `400 Bad Request` | Verify redemption eligibility checks. |
| **LOY-02** | `/api/v1/loyalty/redeem`| POST | `{"points": 0}` | `400 Bad Request` | Verify minimum redemption limit (at least 1 point). |
| **WALL-03** | `/api/v1/wallet/add` | POST | `{"amount": 100001}` | `400 Bad Request` | Verify maximum top-up boundary ($100,000). |

### 1.6 Orders & Support Tickets
Testing life-cycle transitions and invariant checks.

| ID | Endpoint | Method | Input (Context) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ORD-01** | `/api/v1/orders/{id}/cancel`| POST| Cancel "Delivered" order | `400 Bad Request` | Verify order state immutability after delivery. |
| **ORD-02** | `/api/v1/orders/{id}/cancel`| POST| Cancel "Cancelled" order | `400 Bad Request` | Verify state machine idempotency/strictness. |
| **ORD-03** | `/api/v1/orders/999/invoice`| GET | Request missing invoice | `404 Not Found` | Verify consistency of resource discovery errors. |
| **SUPP-01** | `/api/v1/support/ticket` | POST | `{"subject": "Hi", ...}` | `400 Bad Request` | Verify subject length constraint (min 5 chars). |
| **SUPP-02** | `/api/v1/support/tickets/{id}`| PUT | `status: OPEN -> CLOSED` | `400 Bad Request`| Verify status transition (must go through IN_PROGRESS). |
| **SUPP-03** | `/api/v1/support/tickets/{id}`| PUT | `subject: "New Sub" (CLOSED)` | `400 Bad Request`| Verify field immutability for final-state tickets. |
| **REV-04** | `/api/v1/reviews/average` | GET | Multiple ratings (5 and 4) | `average_rating: 4.5` | Verify mathematical calculation accuracy. |

---

---

## 2. Automated Test Execution

The automated test suite was executed using Pytest and Requests against the live API at `http://localhost:8080`.

| Category | Tests | Passed | Failed | Success Rate |
| :--- | :--- | :--- | :--- | :--- |
| Security & Headers | 4 | 3 | 1 | 75% |
| Admin / Data | 2 | 2 | 0 | 100% |
| Profile & Addresses| 9 | 4 | 5 | 44% |
| Product Catalog | 4 | 2 | 2 | 50% |
| Cart & Checkout | 15 | 11 | 4 | 73% |
| Others (Wallet, etc)| 17| 13| 4 | 76% |
| **Total** | **51** | **35** | **16** | **68%** |

---

## 3. Bug Reports

### BUG-01: Cart Quantity Validation Failure
- **Endpoint**: `POST /api/v1/cart/add`
- **Expected Result**: `400 Bad Request` for quantity 0.
- **Actual Result**: `200 OK`.

### BUG-02: Incorrect Status Code for Missing Product
- **Endpoint**: `GET /api/v1/products/999999`
- **Expected Result**: `404 Not Found`.
- **Actual Result**: `400 Bad Request`.

### BUG-03: Profile Update Schema Mismatch (Missing Name)
- **Endpoint**: `PUT /api/v1/profile`
- **Expected Result**: Response includes updated `name`.
- **Actual Result**: `name` field is missing from the JSON response.

### BUG-04: Address Creation Schema Mismatch (Missing ID)
- **Endpoint**: `POST /api/v1/addresses`
- **Expected Result**: Response includes the newly assigned `address_id`.
- **Actual Result**: `address_id` is missing, making it impossible to reference the address in later calls.

### BUG-05: Illegal State Transition for Tickets
- **Endpoint**: `PUT /api/v1/support/tickets/{id}`
- **Expected Result**: `400 Bad Request` when skipping from `OPEN` to `CLOSED`.
- **Actual Result**: `200 OK` (Allowed direct transition, violating one-way state rules).

### BUG-06: Inconsistent Authentication Requirements
- **Endpoint**: `GET /api/v1/products`
- **Expected Result**: Constant header requirements regardless of query parameters.
- **Actual Result**: Adding `?sort=price_asc` triggers a mandatory `X-User-ID` check that is not present on the base endpoint.

### BUG-07: Admin Product Schema Mismatch (Missing Stock)
- **Endpoint**: `GET /api/v1/admin/products`
- **Expected Result**: Each product object includes a `stock` field.
- **Actual Result**: `stock` field is missing, preventing inventory auditing.

### BUG-08: Invoice Schema Mismatch (Missing GST)
- **Endpoint**: `GET /api/v1/orders/{id}/invoice`
- **Expected Result**: Invoice shows the `gst` amount.
- **Actual Result**: `gst` field is missing from the response.

### BUG-09: Cart Add Response Schema Mismatch
- **Endpoint**: `POST /api/v1/cart/add`
- **Expected Result**: Full cart state (`items`, `total`) returned.
- **Actual Result**: Only a success message is returned.

### BUG-10: Admin Coupons Schema Mismatch
- **Endpoint**: `GET /api/v1/admin/coupons`
- **Expected Result**: List of coupons with their `code`.
- **Actual Result**: `code` field is missing or incorrectly named.

### BUG-11: Data Validation Failure (Alphanumeric Pincode)
- **Endpoint**: `POST /api/v1/addresses`
- **Expected Result**: `400 Bad Request` for pincode `123A56`.
- **Actual Result**: `200 OK` (Accepted non-digit characters).

### BUG-12: Ticket Immutability Violation
- **Endpoint**: `PUT /api/v1/support/tickets/{id}`
- **Expected Result**: `400 Bad Request` when trying to re-open a `CLOSED` ticket.
- **Actual Result**: `200 OK` (Allowed state change from CLOSED back to OPEN).

### BUG-13: Persistent Data Validation Failure (Address Update)
- **Endpoint**: `PUT /api/v1/addresses/{id}`
- **Expected Result**: `400 Bad Request` for pincode `ABCDEF`.
- **Actual Result**: `200 OK` (Accepted non-digit characters in UPDATE as well as CREATE).

### BUG-14: Lack of Cancellation State Guard
- **Endpoint**: `POST /api/v1/orders/{id}/cancel`
- **Expected Result**: `400 Bad Request` when cancelling an already `CANCELLED` order.
- **Actual Result**: `200 OK` (Allows redundant cancellation operations).

### BUG-15: Critical Security Vulnerability (Broken Access Control)
- **Endpoint**: `PUT /api/v1/support/tickets/{id}`
- **Expected Result**: `403 Forbidden` when User A attempts to update User B's ticket.
- **Actual Result**: `200 OK` (User A successfully updated someone else's ticket status).

### BUG-16: API Crash on Review Average Calculation
- **Endpoint**: `GET /api/v1/reviews/average`
- **Expected Result**: Valid JSON response with the calculated average.
- **Actual Result**: `500 Internal Server Error` (Returned non-JSON empty response when multiple reviews exist).
