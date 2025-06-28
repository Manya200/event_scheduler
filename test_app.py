import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_create_event(client):
    response = client.post('/events', json={
        "title": "Pytest Event",
        "description": "Testing event creation",
        "start_time": "2025-06-28T16:00:00",
        "end_time": "2025-06-28T17:00:00"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "event" in data
    assert data["event"]["title"] == "Pytest Event"

def test_get_events(client):
    response = client.get('/events')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_update_event(client):
    # First create
    create = client.post('/events', json={
        "title": "To Update",
        "description": "Will change title",
        "start_time": "2025-06-28T17:00:00",
        "end_time": "2025-06-28T18:00:00"
    })
    event_id = create.get_json()['event']['id']

    # Then update
    update = client.put(f'/events/{event_id}', json={
        "title": "Updated Title"
    })
    assert update.status_code == 200
    assert update.get_json()['event']['title'] == "Updated Title"

def test_delete_event(client):
    # First create
    create = client.post('/events', json={
        "title": "To Delete",
        "description": "Will be deleted",
        "start_time": "2025-06-28T19:00:00",
        "end_time": "2025-06-28T20:00:00"
    })
    event_id = create.get_json()['event']['id']

    # Then delete
    delete = client.delete(f'/events/{event_id}')
    assert delete.status_code == 200
    assert "Event deleted" in delete.get_json()['message']
