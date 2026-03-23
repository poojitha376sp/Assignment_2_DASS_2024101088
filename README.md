# DASS Assignment 2 - Software Testing (2024101088)

This repository contains the complete submission for Assignment 2:

1. White box testing for MoneyPoly
2. Integration testing for StreetRace Manager
3. Black box API testing for QuickCart

**Git Repository**: [https://github.com/poojitha376sp/Assignment_2_DASS_2024101088.git](https://github.com/poojitha376sp/Assignment_2_DASS_2024101088.git)
**OneDrive Link**: https://iiithydstudents-my.sharepoint.com/:u:/g/personal/poojitha_j_students_iiit_ac_in/IQCpHeRt3mEIQbypsQkdjrNAAWro55DtktmB5cF9dIPMCMQ?e=2JnReD

---

### **Important Note on Commit History & Hidden Files**
- **Git History**: This repository includes the **`.git`** folder. It is required so that graders can verify the commit history (e.g., "Iteration #:" and "Error #:" commits).
- **Hidden Folder**: Please note that `.git` is a **hidden folder** by default on most systems. To verify its presence in the terminal, use:
  ```bash
  ls -la  # or
  ls -d .git
  ```
- **Log Verification**: To view the commit history, run:
  ```bash
  git log --oneline
  ```

---

## Repository Layout

- `whitebox/` - MoneyPoly source, tests, report.pdf, and diagrams
- `integration/` - StreetRace Manager source, tests, and report.pdf
- `blackbox/` - QuickCart API tests and report.pdf
- `README.md` - this top-level run guide for the whole assignment

---

## Prerequisites

You only need a standard Python environment plus Docker for the black-box part.

Recommended versions:

- Python 3.12 or newer
- `pip`
- `pytest`
- `pylint`
- `requests`
- Docker Desktop or Docker Engine for QuickCart

If you are setting up a fresh environment, the following commands are enough:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pytest pylint requests
```

If your machine already has the packages installed, you can skip the virtual environment and use your existing Python setup.

---

## How To Run Everything

The safest way to verify the whole assignment is to run the three parts in this order:

1. White box tests and linting
2. Integration tests
3. Black box API tests

This order is useful because the white-box part is the most code-heavy and gives immediate feedback about the MoneyPoly logic and report.

---

## Part 1 - White Box Testing for MoneyPoly

This part lives in `whitebox/` and contains:

- `whitebox/code/moneypoly/` - the MoneyPoly game engine (also in the clouds in the CFG, it is just the explanation of that node that it contains.)
- `whitebox/tests/` - pytest-based white-box test batches
- `whitebox/report.pdf` - the detailed report with test cases, errors, commits, and explanations

### 1. Enter the whitebox folder

```bash
cd whitebox
```

### 2. Set the import path

The tests import the local `moneypoly` package directly from `whitebox/code`, so `PYTHONPATH` must point there.

```bash
export PYTHONPATH="$PWD/code"
```

If you are running only one command, you can also prefix it inline:

```bash
PYTHONPATH=code pytest -q tests
```

### 3. Run all white-box tests

```bash
PYTHONPATH=code pytest -q tests
```

This runs every MoneyPoly white-box batch, including the latest regression tests.

### 4. Run a specific white-box batch

If you want to verify one area only, run the corresponding file directly.

Examples:

```bash
PYTHONPATH=code pytest -q tests/test_moneypoly.py
PYTHONPATH=code pytest -q tests/test_moneypoly_batch17.py
```

### 5. Run linting on the MoneyPoly source

```bash
PYTHONPATH=code pylint code/moneypoly/
```

The goal of the white-box part is not only to pass tests, but also to keep the game engine readable, structured, and stable under edge-case inputs.

### White-box focus areas

The report and tests cover:

- movement and Go salary handling
- jail logic and jail card behavior
- property purchase, trade, mortgage, and unmortgage flows
- rent and monopoly rent rules
- bankruptcy cleanup
- card-driven state changes
- board and bank helper functions
- empty-game and boundary safety

---

## Part 2 - Integration Testing for StreetRace Manager

This part lives in `integration/` and checks that the modules work together correctly.

### 1. Enter the integration folder

```bash
cd integration
```

### 2. Set the import path

The integration tests expect the project root to be importable.

```bash
export PYTHONPATH="$PWD/.."
```

### 3. Run all integration tests

```bash
PYTHONPATH=.. pytest -q tests
```

### Integration focus areas

The integration work verifies that cross-module state updates stay consistent, for example:

- registration feeding the crew and inventory modules
- race results updating money and outcomes correctly
- missions depending on the correct crew roles
- trophies and sponsorship logic staying in sync with race events

The matching documentation for this part is in `integration/report.pdf`.

---

## Part 3 - Black Box API Testing for QuickCart

This part lives in `blackbox/` and tests the API exactly as a client would use it.

### 1. Start the QuickCart server

The API tests need the backend running first.

```bash
docker load -i quickcart_image.tar
docker run -d -p 8080:8080 --name quickcart quickcart
```

If the container already exists, stop or remove it before creating a new one.

### 2. Run the API tests

```bash
cd blackbox
pytest -q tests
```

### 3. Stop the container when finished

```bash
docker stop quickcart
docker rm quickcart
```

### Black-box focus areas

The API suite checks:

- valid and invalid request payloads
- header handling such as `X-Roll-Number` and `X-User-ID`
- boundary conditions
- authorization and privilege checks
- schema correctness and error responses

The matching documentation for this part is in `blackbox/report.pdf`.

---

## Suggested Full Verification Sequence

If you want one clean end-to-end run, use this sequence from the repository root:

```bash
source .venv/bin/activate

cd whitebox
PYTHONPATH=code pytest -q tests
PYTHONPATH=code pylint code/moneypoly/

cd ../integration
PYTHONPATH=.. pytest -q tests

cd ../blackbox
docker load -i ../quickcart_image.tar
docker run -d -p 8080:8080 --name quickcart quickcart
pytest -q tests
docker stop quickcart
docker rm quickcart
```

That is the most direct way to verify the whole assignment the same way a TA would inspect it.

---

## Methodology Summary

### White Box

The MoneyPoly work focused on CFG coverage, edge-case coverage, and defect-driven regression tests. Each discovered logic error was fixed and then retested with a dedicated regression case.

### Integration

The StreetRace Manager work focused on module interaction, shared state, and end-to-end behavior across the 9-module design.

### Black Box

The QuickCart work focused on API behavior from the outside, including valid and invalid requests, security-relevant cases, and boundary conditions.

---

## Reports and Evidence

- `whitebox/report.pdf` contains the white-box test table, bug log, and commit mapping
- `integration/report.pdf` contains the integration testing evidence
- `blackbox/report.pdf` contains the API testing findings and bug summary

---

## Troubleshooting

- If Python cannot import `moneypoly`, make sure `PYTHONPATH=code` is set inside `whitebox/`.
- If the integration tests cannot find modules, run them from `integration/` with `PYTHONPATH=..`.
- If Docker says the `quickcart` container already exists, remove it before starting a new one.
- If `pytest` or `pylint` is missing, install them into your active Python environment with `pip install pytest pylint requests`.

---

**Author**: 2024101088
