from fastapi.testclient import TestClient

def test_login_with_invalid_credentials(client: TestClient):
    response = client.post(
        "/users/login",
        json={"username": "ghost", "password": "wrong"}
    )
    assert response.status_code == 400
    assert "Invalid credentials" in response.text