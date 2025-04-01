def test_link_stats(client):
    client.post("/users/", json={"username": "statsuser", "password": "pass"})
    token = client.post("/users/login", json={"username": "statsuser", "password": "pass"}).json()["access_token"]
    
    create_resp = client.post(
        "/links/",
        json={"original_url": "https://stats-test.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    short_code = create_resp.json()["short_code"]
    
    stats_resp = client.get(f"/links/{short_code}/stats")
    assert stats_resp.status_code == 200
    assert stats_resp.json()["clicks"] == 0
    
    response = client.get(f"/links/{short_code}", follow_redirects=False)
    assert response.status_code in (302, 307)
    
    updated_stats = client.get(f"/links/{short_code}/stats").json()
    assert updated_stats["clicks"] == 1