from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_rejects_message_without_link():
    response = client.post("/posting", json={"message": "Hello world"})
    assert response.status_code == 422

def test_rejects_multiple_links():
    response = client.post(
        "/posting",
        json={"message": "Visit https://example.com and https://example.org"},
    )
    assert response.status_code == 422

def test_rejects_message_over_200_characters():
    response = client.post(
        "/posting",
        json={"message": "A" * 190 + " https://example.com"},
    )
    assert response.status_code == 422

def test_rejects_invalid_url():
    response = client.post("/posting", json={"message": "Visit https://not-a-valid-host"})
    assert response.status_code == 422
