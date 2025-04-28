def test_create_contract(client):
    response = client.post(
        "/contracts/",
        json={
            "client_name": "Test Client",
            "cargo_type": "Electronics",
            "destination": "Porto",
            "price": 5000.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["client_name"] == "Test Client"
    assert data["cargo_type"] == "Electronics"
    assert "id" in data


def test_get_contract(client):
    response = client.get("/contracts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["client_name"] == "Test Client"
