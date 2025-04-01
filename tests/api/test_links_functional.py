from fastapi.testclient import TestClient
import pytest
from app.db.database import SessionLocal
from app.models.link import Link

@pytest.fixture
def auth_client(client: TestClient):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    client.post("/users/", json=user_data)

    login_response = client.post("/users/login", json=user_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    client.headers = {"Authorization": f"Bearer {token}"}
    return client

def test_create_link(auth_client: TestClient):
    response = auth_client.post("/links/", json={"original_url": "https://example.com"})
    assert response.status_code == 200
    assert "short_code" in response.json()

def test_create_link_invalid_url(auth_client: TestClient):
    response = auth_client.post("/links/", json={"original_url": "invalid_url"})
    assert response.status_code == 422

def test_get_link_stats(auth_client: TestClient):
    response = auth_client.post("/links/", json={"original_url": "https://example.com"})
    short_code = response.json()["short_code"]

    response = auth_client.get(f"/links/{short_code}/stats")
    assert response.status_code == 200
    assert response.json()["original_url"] == "https://example.com"

def test_update_link(auth_client: TestClient):
    response = auth_client.post("/links/", json={"original_url": "https://example.com"})
    short_code = response.json()["short_code"]

    update_response = auth_client.put(f"/links/{short_code}", json={"original_url": "https://newexample.com"})
    assert update_response.status_code == 200
    assert update_response.json()["original_url"] == "https://newexample.com"

    get_response = auth_client.get(f"/links/{short_code}/stats")
    assert get_response.status_code == 200
    assert get_response.json()["original_url"] == "https://newexample.com"

def test_delete_link(auth_client: TestClient):
    response = auth_client.post("/links/", json={"original_url": "https://example.com"})
    short_code = response.json()["short_code"]

    delete_response = auth_client.delete(f"/links/{short_code}")
    assert delete_response.status_code == 204

    get_response = auth_client.get(f"/links/{short_code}/stats")
    assert get_response.status_code == 404

    response = auth_client.post("/links/", json={"original_url": "https://example.com"})
    short_code = response.json()["short_code"]

    db = SessionLocal()
    db_link = db.query(Link).filter(Link.short_code == short_code).first()
    assert db_link is not None
    assert db_link.original_url == "https://example.com"

    response = auth_client.get(f"/links/{short_code}", follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"] == "https://example.com"