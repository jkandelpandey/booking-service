from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)
bookings = {}
# Trigger CI/CD

@app.route("/bookings", methods=["POST"])
def create_booking():
    data = request.get_json()

    if not data.get("user") or not data.get("destination"):
        return jsonify({"error": "User and destination are required"}), 400

    booking_id = str(uuid.uuid4())
    bookings[booking_id] = {
        "id": booking_id,
        "user": data.get("user"),
        "destination": data.get("destination"),
        "status": "confirmed! You are Going!"
    }

    # Notify via notification-service
    try:
        requests.post("http://notification-service:5002/notify/email", json={
            "to": data.get("user"),
            "message": f"Booking confirmed for {data.get('destination')}"
        }, timeout=3)
    except Exception as e:
        app.logger.error(f"Notification failed: {e}")

    return jsonify(bookings[booking_id]), 201

@app.route("/bookings/<booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(booking), 200

@app.route("/bookings/<booking_id>", methods=["PATCH"])
def update_booking(booking_id):
    data = request.get_json()
    booking = bookings.get(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    if "status" in data:
        booking["status"] = data["status"]
    return jsonify(booking), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
