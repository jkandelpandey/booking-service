import subprocess
import time
import requests
import os
import signal

base_url = "http://localhost:5001"

# Start the app in a subprocess
app_process = subprocess.Popen(["python", "booking_service.py"])
time.sleep(3)  # wait for server to start

def test_create_booking():
    response = requests.post(f"{base_url}/bookings", json={
        "user": "test@example.com",
        "destination": "Paris"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["user"] == "test@example.com"
    assert data["destination"] == "Paris"
    assert "confirmed" in data["status"]

def test_get_booking_not_found():
    response = requests.get(f"{base_url}/bookings/invalid-id")
    assert response.status_code == 404
    assert "error" in response.json()

# Teardown: stop the app after tests
def teardown_module(module):
    os.kill(app_process.pid, signal.SIGTERM)
