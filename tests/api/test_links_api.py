from fastapi.testclient import TestClient

def test_create_and_retrieve_link(client: TestClient):
    user_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    client.post("/users/", json=user_data)

    login_response = client.post("/users/login", json=user_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.post(
        "/links/", 
        json={"original_url": "https://example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    short_code = response.json()["short_code"]
    
    response = client.get(f"/links/{short_code}/stats")
    assert response.status_code == 200
    assert response.json()["original_url"] == "https://example.com"
