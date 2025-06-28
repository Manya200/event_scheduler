# 🗓️ Event Scheduler System – Flask Backend Application

A simple and powerful event scheduling REST API built with **Python 3.x** and **Flask**, enabling users to manage events with features like:

- 📌 Create, View, Update, Delete Events
- 🔁 Recurring Events (Daily, Weekly, Monthly)
- 🔍 Search Events by Title or Description
- 🔔 Console Reminders for Upcoming Events (within 1 hour)
- 📧 Email Notifications *(optional, SMTP ready)*
- 🧪 Fully Tested with Pytest
- ✅ Postman Collection for easy testing

---

## 🚀 Getting Started

### 📦 Requirements

- Python 3.7+
- pip (Python package manager)

### 📁 Installation

```bash
git clone https://github.com/your-username/event-scheduler.git
cd event-scheduler
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
python app.py
```

App runs locally at:
```
http://localhost:5000/
```

---

## 📬 API Endpoints

| Method | Endpoint                  | Description                     |
|--------|---------------------------|---------------------------------|
| GET    | `/events`                | List all events (sorted)       |
| POST   | `/events`                | Create a new event             |
| PUT    | `/events/<event_id>`     | Update an existing event       |
| DELETE | `/events/<event_id>`     | Delete an event                |
| GET    | `/events/search?query=`  | Search events by title/desc    |

---

## 📌 Request Example (POST `/events`)

```json
{
  "title": "Doctor Appointment",
  "description": "Visit Dr. Sharma",
  "start_time": "2025-06-28T14:00:00",
  "end_time": "2025-06-28T15:00:00",
  "recurrence": "daily",                // Options: none, daily, weekly, monthly
  "email": "youremail@example.com"     // Optional: for email reminders
}
```

---

## 🔁 Recurring Events

Supports these recurrence types:
- `"daily"`
- `"weekly"`
- `"monthly"`
- `"none"` *(default)*

---

## 🔔 Reminders

- A background thread checks every **60 seconds**
- If any event is due within **next 1 hour**, it:
  - 📢 Prints reminder in terminal
  - 📧 Sends email (if email provided and SMTP configured)

---

## 📧 Email Notifications *(Optional)*

- Email feature uses Gmail SMTP
- Configure in `send_email()` function inside `app.py`
```python
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
```
- ⚠️ Do **not share** credentials; use [App Passwords](https://myaccount.google.com/apppasswords) if needed

---

## 🧪 Running Tests

Tests written using **Pytest** in `test_app.py`

```bash
pip install -r requirements.txt
pytest test_app.py
```

---

## 📥 Postman Collection

A Postman collection is included for all endpoints:

📁 **`EventSchedulerCollection.postman_collection.json`**

- Import into Postman using `Import → Upload Files`
- Test all CRUD + Search endpoints easily

---

## 📂 Project Structure

```
event-scheduler/
├── app.py                          # Main Flask app
├── events.json                     # Data store (JSON file)
├── test_app.py                     # Unit tests using Pytest
├── requirements.txt
├── README.md
└── EventSchedulerCollection.postman_collection.json
```

---

## ✅ Submission Checklist

- [x] Python 3.x Flask backend
- [x] CRUD operations
- [x] File persistence
- [x] Reminder every minute
- [x] Recurring events
- [x] Email (optional)
- [x] Search API
- [x] Postman collection
- [x] Unit tests with Pytest
- [x] Professional README

---

## 👨‍💻 Developed By

**Manish Gamare**  
Python & Django Developer  
[LinkedIn](http://www.linkedin.com/in/manish-gamare-889833251) • [GitHub](https://github.com/Manya200)

---

## 📄 License

This project is for educational and evaluation purposes under the BIZ Technology challenge.