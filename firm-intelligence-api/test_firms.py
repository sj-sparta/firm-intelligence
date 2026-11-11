"""Contract tests for /firms. No keys, no network. Each test makes its own data."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

VALID_FIRM = {"name": "Test Co", "jurisdiction": "UK", "revenue_usd_m": 100,
              "lawyers": 50, "equity_partners": 10}


def test_list_firms_returns_200_and_a_list():
    response = client.get("/firms")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_missing_firm_returns_404():
    response = client.get("/firms/999")
    assert response.status_code == 404


def test_invalid_firm_is_rejected_with_422():
    bad = {**VALID_FIRM, "jurisdiction": "X"}
    response = client.post("/firms", json=bad)
    assert response.status_code == 422


def test_create_firm_returns_201_and_appears_in_list():
    response = client.post("/firms", json=VALID_FIRM)
    assert response.status_code == 201
    new_id = response.json()["id"]

    listing = client.get("/firms").json()
    assert any(f["id"] == new_id for f in listing)


def test_update_firm_returns_200_and_persists():
    created = client.post("/firms", json=VALID_FIRM).json()
    changed = {**VALID_FIRM, "name": "Updated Co"}

    response = client.put(f"/firms/{created['id']}", json=changed)
    assert response.status_code == 200
    assert client.get(f"/firms/{created['id']}").json()["name"] == "Updated Co"


def test_delete_firm_returns_204_then_404():
    created = client.post("/firms", json=VALID_FIRM).json()

    assert client.delete(f"/firms/{created['id']}").status_code == 204
    assert client.get(f"/firms/{created['id']}").status_code == 404


def test_retried_post_with_same_idempotency_key_does_not_duplicate():
    headers = {"Idempotency-Key": "test-key-123"}
    payload = {**VALID_FIRM, "name": "Retry Co"}

    first = client.post("/firms", json=payload, headers=headers)
    second = client.post("/firms", json=payload, headers=headers)

    assert first.json()["id"] == second.json()["id"]
    matches = [f for f in client.get("/firms").json() if f["name"] == "Retry Co"]
    assert len(matches) == 1