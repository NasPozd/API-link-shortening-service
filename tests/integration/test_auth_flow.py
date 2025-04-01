def test_full_auth_flow(client):
    client.post("/users/", json={"username": "authuser", "password": "authpass"})
    
    login_resp = client.post("/users/login", json={"username": "authuser", "password": "authpass"})
    token = login_resp.json()["access_token"]
    
    link_resp = client.post(
        "/links/",
        json={"original_url": "https://auth-test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert link_resp.status_code == 200
    assert link_resp.json()["user_id"] is not None