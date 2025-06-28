from flask import Flask, request, jsonify
import json
import uuid
from datetime import datetime
import os

app = Flask(__name__)
DATA_FILE = 'events.json'

import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# Load or initialize
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Helper: load events
def load_events():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Helper: save events
def save_events(events):
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=4)

# 🔁 GET: List all events (sorted)
@app.route('/events', methods=['GET'])
def get_events():
    events = load_events()
    events.sort(key=lambda x: x['start_time'])
    return jsonify(events)

# ➕ POST: Create event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    required = ['title', 'description', 'start_time', 'end_time']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    try:
        # Parse to validate datetime
        start = datetime.fromisoformat(data['start_time'])
        end = datetime.fromisoformat(data['end_time'])
        if end <= start:
            return jsonify({"error": "End time must be after start time"}), 400
    except ValueError:
        return jsonify({"error": "Invalid datetime format"}), 400

    event = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "description": data['description'],
        "start_time": data['start_time'],
        "end_time": data['end_time'],
        "recurrence": data.get("recurrence", "none").lower(),
        "email": data.get("email", "")
    }



    events = load_events()
    events.append(event)
    save_events(events)
    return jsonify({"message": "Event created", "event": event}), 201

# ✏️ PUT: Update event
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    events = load_events()
    for event in events:
        if event['id'] == event_id:
            event.update({k: data[k] for k in data if k in event})
            save_events(events)
            return jsonify({"message": "Event updated", "event": event})
    return jsonify({"error": "Event not found"}), 404

# 🗑 DELETE: Remove event
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events = load_events()
    updated_events = [e for e in events if e['id'] != event_id]
    if len(updated_events) == len(events):
        return jsonify({"error": "Event not found"}), 404
    save_events(updated_events)
    return jsonify({"message": "Event deleted"})

import threading
import time

# ⏰ Background Reminder Thread
def reminder_checker():
    while True:
        events = load_events()
        now = datetime.now()
        upcoming = []

        for event in events:
            try:
                start_time = datetime.fromisoformat(event['start_time'])

                # 🔁 Check if it's a recurring event and adjust date to today
                recurrence = event.get("recurrence", "none")
                if recurrence == "daily":
                    start_time = start_time.replace(year=now.year, month=now.month, day=now.day)
                elif recurrence == "weekly":
                    days_diff = (now.weekday() - start_time.weekday()) % 7
                    adjusted_date = now.date()
                    start_time = datetime.combine(adjusted_date, start_time.time())
                elif recurrence == "monthly":
                    start_time = start_time.replace(year=now.year, month=now.month)

                diff = (start_time - now).total_seconds()
                if 0 <= diff <= 3600:
                    upcoming.append(event)

            except Exception as e:
                continue

        if upcoming:
            print("\n🔔 Upcoming Events within 1 hour:")
            for e in upcoming:
                msg = f"Reminder: '{e['title']}' is starting at {e['start_time']}\n\nDetails:\n{e['description']}"
                print(f"📅 {e['title']} at {e['start_time']} - {e['description']}")

                if e.get("email"):
                    send_email(e["email"], f"Reminder: {e['title']}", msg)


        time.sleep(60)


# 🔍 Search events by title or description
@app.route('/events/search', methods=['GET'])
def search_events():
    query = request.args.get('query', '').lower()

    if not query:
        return jsonify({"error": "Please provide a query parameter"}), 400

    events = load_events()
    filtered = [
        e for e in events
        if query in e['title'].lower() or query in e['description'].lower()
    ]

    return jsonify(filtered)





if __name__ == '__main__':
    # Start reminder thread
    reminder_thread = threading.Thread(target=reminder_checker, daemon=True)
    reminder_thread.start()

    # Run Flask app
    app.run(debug=True)
