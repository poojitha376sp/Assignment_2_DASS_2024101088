# QuickCart Black-Box API Testing Report

This report documents the test case design, execution results, and bug reports for the QuickCart REST API.

---

## 1. Test Case Design

### 1.1 Header & Security Validation
Every request must include `X-Roll-Number`. User-scoped endpoints also require `X-User-ID`.

| ID | Scenario [Type] | Input | Expected Output (Status / JSON / Data) | Justification & Importance |
| :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Missing Roll No **[M]** | No `X-Roll-Number` | `401 Unauthorized` | Ensures mandatory system-wide access control. |
| **SEC-02** | Invalid Roll Type **[T]** | `X-Roll-Number`: "ABC" | `400 Bad Request` | Verifies data type safety for system headers. |
| **SEC-03** | Missing User ID **[M]** | No `X-User-ID` | `400 Bad Request` | Ensures user-scoped data cannot be accessed anonymously. |
| **SEC-04** | Negative User ID **[B]**| `X-User-ID`: -5 | `400 Bad Request` | Verifies positive integer boundaries. |
| **SEC-05** | Auth Leak **[I]**| Regular user hit Admin| `403 Forbidden` | Critical for privilege escalation prevention. |
| **SEC-06** | Access Control **[I]**| User A hits User B tkt| `403 Forbidden` | Ensures cross-user data isolation. |
| **SEC-07** | No Headers **[M]** | Empty Headers | `401 Unauthorized` | Verifies default rejection of unauthenticated traffic. |

### 1.2 Profile & Address Management
Validating constraints on user-supplied data and address invariants.

| ID | Scenario [Type] | Input | Expected Output (Status / JSON / Data) | Justification & Importance |
| :--- | :--- | :--- | :--- | :--- |
| **PROF-01**| Min Name Length **[B]**| `name`: "A" | `400 Bad Request` | Ensures realistic identity data (min 2 chars). |
| **PROF-02**| Phone Length **[B]** | `phone`: "123" | `400 Bad Request` | Ensures exact 10-digit mobile format. |
| **PROF-03**| Phone Type **[T]** | `phone`: 1234567890 | `400 Bad Request` | Verifies JSON string constraint for phone fields. |
| **ADDR-01**| Enum Violation **[I]** | `label`: "VACATION" | `400 Bad Request` | Verifies adherence to allowed address types. |
| **ADDR-02**| Pincode Length **[B]** | `pincode`: "12345" | `400 Bad Request` | Verifies exact 6-digit postal code constraint. |
| **ADDR-03**| Pincode Format **[I]** | `pincode`: "12A456" | `400 Bad Request` | Verifies digit-only constraint for logistics. |
| **ADDR-04**| Default Swap **[V]** | Set 2nd default | `200` + Prev unset | Verifies "single default" business logic. |
| **ADDR-05**| Missing Field **[M]** | `{pincode: 123456}`| `400 Bad Request` | Ensures all components of an address are present. |

### 1.3 Product Catalog
Testing visibility, search accuracy, and sorting logic for consumer-facing browse features.

| ID | Scenario [Type] | Input | Expected Output (Status / JSON / Data) | Justification & Importance |
| :--- | :--- | :--- | :--- | :--- |
| **PROD-01**| State Filtering **[V]**| Base URL | List where `active: True` | Ensures consumers don't see unlisted items. |
| **PROD-02**| Resource Discovery **[I]**| ID: 9999 | `404 Not Found` | Verifies graceful error handling for missing items. |
| **PROD-03**| Sort Numerics **[V]** | `?sort=price_asc` | JSON array, `p[i] <= p[i+1]` | Verifies numerical sorting and API correctness. |
| **PROD-04**| Matrix Search **[V]** | `?cat=X&q=Y` | Combined results | Verifies multi-parameter query processing. |
| **PROD-05**| Inactive Lookup **[I]**| ID: [Inactive] | `404 Not Found` | Ensures single-item lookup honors state rules. |
| **PROD-06**| String Fuzzing **[I]**| `search`: "'--" | `200/400` (No 500) | Verifies sanitization against SQL Injection. |

### 1.4 Cart & Checkout Logic
Verifying stateful transitions, inventory guards, and financial logic.

| ID | Scenario [Type] | Input | Expected Output (Status / JSON / Data) | Justification & Importance |
| :--- | :--- | :--- | :--- | :--- |
| **CART-01**| Min Quantity **[B]**| `quantity`: 0 | `400 Bad Request` | Prevents nonsensical 0-item additions. |
| **CART-02**| Inventory Stock **[B]**| `qty`: 999999 | `400 Bad Request` | Essential guard against overselling. |
| **CART-03**| State Merge **[V]** | Add existing | Merged quantities | Verifies correct state accumulation logic. |
| **CART-04**| Null Quantity **[T]** | `qty`: null | `400 Bad Request` | Verifies type-safety for cart transactions. |
| **COUP-01**| Min Threshold **[B]**| `SAVE10` < $500| `400 Bad Request` | Verifies minimum cart value rule enforcement. |
| **COUP-02**| Discount Caps **[B]**| Huge cart val| `total = max_cap` | Verifies maximum discount cap enforcement. |
| **CHCK-01**| Payment Filter **[I]**| `meth`: BTC | `400 Bad Request` | Ensures only white-listed payment methods. |
| **CHCK-02**| COD Threshold **[B]**| Value > $5000 | `400 Bad Request` | Critical anti-fraud and risk management rule. |
| **FIN-01** | Tax Precision **[V]** | Valid Order | `Total = Sub + 5% GST`| Ensures financial accuracy and legal compliance. |

### 1.5 Wallet & Loyalty Points
Testing balance management and point redemption invariants.

| ID | Scenario [Type] | Input | Expected Output (Status / JSON / Data) | Justification & Importance |
| :--- | :--- | :--- | :--- | :--- |
| **WALL-01**| Low Balance **[B]** | `pay`: $10^6$ | `400 Bad Request` | Validates insufficient funds handling. |
| **WALL-02**| Sign Check **[B]** | `add`: -$10$ | `400 Bad Request` | Prevents balance reduction via top-up. |
| **WALL-03**| Maximum Top-up **[B]**| `add`: $100001$| `400 Bad Request` | Prevents runaway balance growth. |
| **LOY-01** | Eligibility **[V]** | Redeem > Bal | `400 Bad Request` | Ensures points are earned before spending. |
| **LOY-02** | Min Redemption **[B]**| `points`: 0 | `400 Bad Request` | Verifies valid transaction thresholds. |

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

### 1.7 Fuzzing & Advanced Stress
Testing system resilience against data-type violations and extreme fuzzing (60+ scenarios).

| ID | Endpoint | Method | Input Variation | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FUZZ-01** | `/api/v1/products` | GET | SQL Injection, XSS, etc | `200/400` (No 500) | Verify sanitization of query parameters. |
| **FUZZ-02** | `/api/v1/cart/add` | POST | `quantity: null/float/str` | `400 Bad Request` | Verify strict type validation for quantities. |
| **FUZZ-03** | `/api/v1/profile` | PUT | String Overflow (>1000 chars)| `400 Bad Request` | Verify buffer/length constraints on inputs. |
| **FUZZ-04** | `/api/v1/addresses` | POST | `pincode: True/None/Object` | `400 Bad Request` | Verify strict type validation for pincodes. |
| **SEC-06** | `/api/v1/wallet/balance`| GET | Request WITHOUT User ID | `400 Bad Request` | Verify identification requirements for private data. |

---

---

## 2. Automated Test Execution

The automated test suite was executed using Pytest and Requests against the live API at `http://localhost:8080`.

| Category | Tests | Passed | Failed | Success Rate |
| :--- | :--- | :--- | :--- | :--- |
| Security & Headers | 20 | 17 | 3 | 85% |
| Admin / Data | 15 | 10 | 5 | 66% |
| Profile & Addresses| 45 | 40 | 5 | 88% |
| Product Catalog | 50 | 47 | 3 | 94% |
| Cart & Checkout | 50 | 43 | 7 | 86% |
| Others (Fuzzing/REV) | 60 | 54 | 6 | 90% |
| **Total** | **240** | **211** | **29** | **88%** |

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
- **Actual Result**: `200 OK` (Bypass successful).

### BUG-16: API Crash on Review Average Calculation
- **Endpoint**: `GET /api/v1/reviews/average`
- **Expected Result**: Valid JSON response.
- **Actual Result**: `500 Internal Server Error` (Crash when >1 review exists).

### BUG-17: Authentication Leak (Missing User Scoping)
- **Endpoint**: `GET /api/v1/wallet/balance`
- **Expected Result**: `400 Bad Request` if `X-User-ID` is missing.
- **Actual Result**: `200 OK` (Leaks wallet balance anonymously).

### BUG-18: Critical Financial Logic Error (Total Zero)
- **Endpoint**: `GET /api/v1/orders/{id}/invoice`
- **Expected Result**: `total` must equal `subtotal + gst`.
- **Actual Result**: `total` is returned as `0` regardless of subtotal.

### BUG-19: GST Calculation Precision Error
- **Endpoint**: `GET /api/v1/orders/{id}/invoice`
- **Expected Result**: `gst` must be exactly 5% of subtotal.
- **Actual Result**: `gst` is consistently returned as `0`.

### BUG-20: Data Type Validation Failure (Null Values)
- **Endpoint**: `POST /api/v1/cart/add`
- **Expected Result**: `400 Bad Request` when `quantity` is `null`.
- **Actual Result**: `200 OK` (Accepted null quantity).

### BUG-21: Inactive Product Visibility Breach
- **Endpoint**: `GET /api/v1/products/{id}`
- **Expected Result**: `404 Not Found` for products marked as `active: False`.
- **Actual Result**: `200 OK` (User can still fetch internal product details if they know the ID).

### BUG-22: Review Logic Violation (Unordered Products)
- **Endpoint**: `POST /api/v1/reviews`
- **Expected Result**: `400 Bad Request` if user has not ordered the product.
- **Actual Result**: `200 OK` (Allows fake reviews for unordered products).

### BUG-23: Review Logic Violation (Duplicate Reviews)
- **Endpoint**: `POST /api/v1/reviews`
- **Expected Result**: `400 Bad Request` for a second review of the same product.
- **Actual Result**: `200 OK` (Allows spamming multiple reviews per product).

### BUG-24: Financial Invariant Violation (Impossible Coupons)
- **Endpoint**: `POST /api/v1/admin/coupons`
- **Expected Result**: `400 Bad Request` for percentage discounts > 100%.
- **Actual Result**: `200 OK`.

### BUG-25: Routing / Parsing Crash (Review Rating)
- **Endpoint**: `POST /api/v1/reviews`
- **Expected Result**: `400 Bad Request` for invalid rating strings like `--`.
- **Actual Result**: `404 Not Found`.

### BUG-26: Business Logic Failure (Coupon Recycling)
- **Endpoint**: `POST /api/v1/coupon/apply`
- **Expected Result**: One-time coupons should be reusable if the order was cancelled.
- **Actual Result**: `400 Bad Request` (Coupon marked as used permanently).

### BUG-27: Admin Logic Failure (Negative Price)
- **Endpoint**: `PUT /api/v1/admin/products/{id}`
- **Expected Result**: `400 Bad Request` when setting price to -100.
- **Actual Result**: `200 OK` (Accepted negative price).

### BUG-28: Admin Logic Failure (Negative Stock)
- **Endpoint**: `PUT /api/v1/admin/products/{id}`
- **Expected Result**: `400 Bad Request` when setting stock to -10.
- **Actual Result**: `200 OK` (Accepted negative stock).

### BUG-29: Critical Security Vulnerability (Privilege Escalation)
- **Endpoint**: `GET /api/v1/admin/users`
- **Expected Result**: `403 Forbidden` for regular users.
- **Actual Result**: `200 OK` (Admin data leaked to all valid roll number holders).
