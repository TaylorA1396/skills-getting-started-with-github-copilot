from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_duplicate_and_delete():
    test_email = "pytest-user@example.com"
    activity = "Chess Club"

    # Ensure not present initially (remove if exists)
    client.delete(f"/activities/{activity}/participants?email={test_email}")

    # Signup should succeed
    r1 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert r1.status_code == 200
    assert test_email in client.get("/activities").json()[activity]["participants"]

    # Signing up again should fail with 400
    r2 = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert r2.status_code == 400

    # Delete should succeed
    r3 = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert r3.status_code == 200
    assert test_email not in client.get("/activities").json()[activity]["participants"]
