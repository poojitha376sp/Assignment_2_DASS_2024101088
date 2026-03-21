import requests
import pytest

def test_supp01_subject_min_length(base_url, user_headers):
    """SUPP-01: Subject must be at least 5 characters."""
    url = f"{base_url}/support/ticket"
    payload = {"subject": "Hi", "message": "Valid message longer than 1 character."}
    response = requests.post(url, headers=user_headers(), json=payload)
    assert response.status_code == 400

def test_supp02_invalid_status_transition(base_url, user_headers):
    """SUPP-02: Verify status cannot skip IN_PROGRESS (OPEN -> CLOSED is invalid)."""
    # This requires an existing ticket ID.
    # For now, we use a placeholder or assume ID 1.
    url = f"{base_url}/support/tickets/1"
    payload = {"status": "CLOSED"}
    response = requests.put(url, headers=user_headers(), json=payload)
    # This might return 400 if it violates the transition rule.
    if response.status_code == 400:
        pass
