# DASS Assignment 2 - Software Testing (Poojitha - 2024101088)

Consolidated repository for White Box, Integration, and Black Box API testing.

**Git Repository**: [https://github.com/poojitha376sp/Assignment_2_DASS_2024101088.git](https://github.com/poojitha376sp/Assignment_2_DASS_2024101088.git)

---

## 🚀 How to Run the Tests

### **1. Part 1: White Box Testing (MoneyPoly)**
Ensure you are in the project root and have the dependencies installed.

**Pylint (Source Quality)**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/whitebox/code/
pylint whitebox/code/moneypoly/
```
*Current Rating: 10.00/10*

**Pytest (Statement/Branch Coverage)**
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/whitebox/code/
pytest whitebox/tests/
```

### **2. Part 3: Black Box API Testing (QuickCart)**
The server must be running (Docker) before execution.

**Start Server**
```bash
docker load -i quickcart_image.tar
docker run -d -p 8080:8080 --name quickcart quickcart
```

**Run Automated API Tests**
```bash
pytest blackbox/tests/
```

---

## 🛠️ Methodology & Implementation Details

### **Part 1: White Box Testing (MoneyPoly)**
1.  **CFG Analysis (Node-by-Node)**: I mapped 78 logical statements defining the entire game engine. This included identifying missing logic for Monopoly house-building (Nodes 48-52 in the design) and implementing it to reach 100% coverage.
2.  **Iterative Pylint Refactoring**: I performed atomic commits for each quality improvement. Starting from ~8/10, I refactored missing docstrings, unused imports, and complex logic flow to achieve a perfect 10.00/10 rating.
3.  **Logical Bug Hunting**: Each test case was designed to trigger specific CFG branches. This revealed 7 critical logical errors (e.g., missing rent transfers, incorrect Go salary boundaries), which were fixed and committed individually.

### **Part 2: Integration Testing (StreetRace Manager)**
*In Progress / Deferred.* Designed 8 interconnected modules including "Vehicle Tuning" and "Sponsorships" to verify complex inter-module communications.

### **Part 3: Black Box API Testing (QuickCart)**
1.  **Scenario Design**: I designed 20+ test scenarios based strictly on the API documentation, covering valid/invalid inputs, header security, and boundary values (e.g., COD limits, name lengths).
2.  **Automation Framework**: Built a modular Pytest suite using `requests`. Implemented shared fixtures in `conftest.py` to handle `X-Roll-Number` and `X-User-ID` headers centrally.
3.  **Expected vs Actual Verification**: Tests verify status codes, JSON structures, and data correctness against the technical specification.

---
**Author**: Poojitha J (2024101088)
