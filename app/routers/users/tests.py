import json

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

from .utils import InterestVector

client = TestClient(app)
client.base_url += "/api/v1"
client.base_url = client.base_url.rstrip("/") + "/"


def mock_get_value(self, user, content, update_type):
    return [0. for i in range(220)]


def test_users_vector_success(monkeypatch):
    data = {"user_id": 24, "content_id": 24, "update_type": "post"}
    monkeypatch.setattr(InterestVector, "get_updated_vector", mock_get_value)
    response = client.post('users/update-user-vector', data=json.dumps(data))
    assert response.status_code == 200
    assert len(response.json()["vector"]) == 220


def test_users_vector_error():
    data = {"user_id": 24, "content_id": 24, "update_type": "post"}
    response = client.post('users/update-user-vector', data=json.dumps(data))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_users_vector_invalid_data():
    data = {"user_id": 4, "content_id": "invalid", "update_type": "post"}
    response = client.post('users/update-user-vector', data=json.dumps(data))
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data["detail"] == "User not found!"


def test_generate_user_vector():
    data = {"categories": ["/Business & Industrial"]}
    response = client.post('users/generate-user-vector', data=json.dumps(data))
    assert response.status_code == 200
    assert len(response.json()["vector"]) == 220
