def test_create_vessel(client):
    response = client.post(
        "/vessels/",
        json={"name": "SS Enterprise", "capacity": 10000, "current_location": "Rio de Janeiro"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SS Enterprise"
    assert data["capacity"] == 10000

def test_get_vessel(client):
    response = client.get("/vessels/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["current_location"] == "Rio de Janeiro"
