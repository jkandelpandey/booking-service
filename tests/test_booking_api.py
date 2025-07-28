import requests

BASE_URL = "http://localhost:5001"

def test_create_booking():
    response = requests.post(f"{BASE_URL}/bookings", json={
        "user": "testuser@example.com",
        "destination": "Paris"
    })
    assert response.status_code == 201
    assert "id" in response.json()

def test_get_booking_not_found():
    response = requests.get(f"{BASE_URL}/bookings/invalid-id")
    assert response.status_code == 404
