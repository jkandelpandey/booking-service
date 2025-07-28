import sys
import os
import pytest

# Add parent directory to sys.path so 'app' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  # Importing from app.py directly

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_booking(client):
    response = client.post("/bookings", json={
        "user": "test@example.com",
        "destination": "Paris"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["user"] == "test@example.com"
    assert data["destination"] == "Paris"
    assert "confirmed" in data["status"]

def test_get_booking_not_found(client):
    response = client.get("/bookings/invalid-id")
    assert response.status_code == 404
    assert "error" in response.get_json()
