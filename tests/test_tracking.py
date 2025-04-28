def test_create_tracking(client):
    response = client.post(
        "/trackings/",
        json={"cargo_id": 1, "location": "Warehouse"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["cargo_id"] == 1
    assert data["location"] == "Warehouse"

def test_get_tracking(client):
    response = client.get("/trackings/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["location"] == "Warehouse"
