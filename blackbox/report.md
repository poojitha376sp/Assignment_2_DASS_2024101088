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

### 1.2 Profile & Address Management
Validating constraints on user-submitted data.

| ID | Endpoint | Method | Input (Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PROF-01** | `/api/v1/profile` | PUT | `{"name": "A", "phone": "1234567890"}` | `400 Bad Request` | Verify name length constraint (min 2 chars). |
| **PROF-02** | `/api/v1/profile` | PUT | `{"name": "Tester", "phone": "123"}` | `400 Bad Request` | Verify phone length constraint (exactly 10 digits). |
| **ADDR-01** | `/api/v1/addresses` | POST | `{"label": "VACATION", ...}` | `400 Bad Request` | Verify enum constraint (HOME, OFFICE, OTHER only). |
| **ADDR-02** | `/api/v1/addresses` | POST | `{"pincode": "1234567"}` | `400 Bad Request` | Verify pincode length constraint (exactly 6 digits). |

### 1.3 Product Catalog
Testing search, filter, and visibility rules.

| ID | Endpoint | Method | Input (Query) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PROD-01** | `/api/v1/products` | GET | None | List of active products only | Verify privacy/state filtering (inactive products hidden). |
| **PROD-02** | `/api/v1/products/9999` | GET | ID: 9999 (Non-existent) | `404 Not Found` | Verify error handling for missing resources. |

### 1.4 Cart & Checkout Logic
Verifying transaction rules and financial correctness.

| ID | Endpoint | Method | Input (Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CART-01** | `/api/v1/cart/add` | POST | `{"product_id": 1, "quantity": 0}` | `400 Bad Request` | Verify minimum quantity constraint. |
| **CART-02** | `/api/v1/cart/add` | POST | `{"product_id": 1, "quantity": 1000}` | `400 Bad Request` | Verify inventory/stock check logic. |
| **COUP-01** | `/api/v1/coupon/apply` | POST | `{"code": "SAVE10"}` (Low Cart Value) | `400 Bad Request` | Verify minimum cart value constraint for coupons. |
| **CHCK-01** | `/api/v1/checkout` | POST | `{"payment_method": "BITCOIN"}` | `400 Bad Request` | Verify restricted payment methods (COD, WALLET, CARD only). |
| **CHCK-02** | `/api/v1/checkout` | POST | `{"payment_method": "COD"}` (Order > 5000) | `400 Bad Request` | Verify COD upper limit constraint ($5000). |
| **FIN-01** | `/api/v1/checkout` | POST | Valid Cart | `GST: 5%` calculation | Verify tax calculation accuracy. |

### 1.5 Wallet & Loyalty Points
Testing balance management and point redemption.

| ID | Endpoint | Method | Input (Body) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WALL-01** | `/api/v1/wallet/pay` | POST | `{"amount": 999999}` | `400 Bad Request` | Verify insufficient balance handling. |
| **WALL-02** | `/api/v1/wallet/add` | POST | `{"amount": -10}` | `400 Bad Request` | Verify positive amount constraint for top-ups. |
| **LOY-01** | `/api/v1/loyalty/redeem`| POST | `{"points": 1}` (Zero balance) | `400 Bad Request` | Verify redemption eligibility checks. |

### 1.6 Orders & Support Tickets
Testing life-cycle transitions and invariant checks.

| ID | Endpoint | Method | Input (Context) | Expected Output | Justification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ORD-01** | `/api/v1/orders/{id}/cancel`| POST| Cancel "Delivered" order | `400 Bad Request` | Verify order state immutability after delivery. |
| **SUPP-01** | `/api/v1/support/ticket` | POST | `{"subject": "Hi", ...}` | `400 Bad Request` | Verify subject length constraint (min 5 chars). |
| **SUPP-02** | `/api/v1/support/tickets/{id}`| PUT | `status: OPEN -> CLOSED` | `400 Bad Request`| Verify status transition (must go through IN_PROGRESS). |

---

---

## 2. Automated Test Execution

The automated test suite was executed using Pytest and Requests against the live API at `http://localhost:8080`.

| Category | Tests | Passed | Failed | Success Rate |
| :--- | :--- | :--- | :--- | :--- |
| Security & Headers | 3 | 3 | 0 | 100% |
| Admin / Data | 2 | 2 | 0 | 100% |
| Profile & Addresses| 6 | 5 | 1 | 83% |
| Product Catalog | 3 | 2 | 1 | 66% |
| Cart & Checkout | 6 | 4 | 2 | 66% |
| Others (Wallet, etc)| 11| 11| 0 | 100% |
| **Total** | **31** | **27** | **4** | **87%** |

---

## 3. Bug Reports

### BUG-01: Cart Quantity Validation Failure
- **Endpoint**: `POST /api/v1/cart/add`
- **Request Payload**: 
  - **Method**: POST
  - **URL**: `http://localhost:8080/api/v1/cart/add`
  - **Body**: `{"product_id": 1, "quantity": 0}`
- **Expected Result**: `400 Bad Request` (Spec: "Sending 0 or a negative number must be rejected with a 400 error.")
- **Actual Result**: `200 OK` (Item added with 0 quantity).

### BUG-02: Incorrect Status Code for Missing Product
- **Endpoint**: `GET /api/v1/products/{product_id}`
- **Request Payload**: 
  - **Method**: GET
  - **URL**: `http://localhost:8080/api/v1/products/999999`
- **Expected Result**: `404 Not Found` (Spec: "returns a 404 error if the product does not exist.")
- **Actual Result**: `400 Bad Request`.

### BUG-03: Profile Update Schema Mismatch
- **Endpoint**: `PUT /api/v1/profile`
- **Request Payload**: 
  - **Method**: PUT
  - **URL**: `http://localhost:8080/api/v1/profile`
  - **Body**: `{"name": "New Name", "phone": "1234567890"}`
- **Expected Result**: JSON response containing the updated profile including `name`.
- **Actual Result**: `{"phone": "1234567890", "message": "Profile updated successfully"}` (Missing `name` field).

### BUG-04: Cart Add Response Schema Mismatch
- **Endpoint**: `POST /api/v1/cart/add`
- **Request Payload**: 
  - **Method**: POST
  - **URL**: `http://localhost:8080/api/v1/cart/add`
  - **Body**: `{"product_id": 1, "quantity": 2}`
- **Expected Result**: JSON response containing the full cart items and total.
- **Actual Result**: `{"message": "Item added to cart"}` (Missing `items` and `total` fields).
