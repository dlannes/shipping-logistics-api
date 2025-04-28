def test_create_cargo(client):
    response = client.post(
        "/cargos/",
        json={"contract_id": 1, "status": "pending"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["contract_id"] == 1
    assert data["status"] == "pending"

def test_get_cargo(client):
    response = client.get("/cargos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["status"] == "pending"
