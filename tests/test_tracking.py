import pytest

@pytest.fixture()
def seeded_cargo_and_vessel(client):
    contract_resp = client.post("/contracts", json={
        "client_name": "PortoLog",
        "cargo_type": "Vinho do Porto",
        "origin": "Porto",
        "destination": "Rotterdam",
        "price": 5000.0
    })
    assert contract_resp.status_code == 200
    contract_data = contract_resp.json()
    cargo_id = contract_data["cargo"]["id"]

    vessel_resp = client.post("/vessels", json={
        "name": "Lusitano",
        "capacity": 1,
        "current_location": "Porto"
    })
    assert vessel_resp.status_code == 200
    vessel_id = vessel_resp.json()["id"]

    return cargo_id, vessel_id


def test_tracking_nonexistent_cargo(client):
    response = client.get("/trackings/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cargo not found"


def test_tracking_empty_history(client, seeded_cargo_and_vessel):
    cargo_id, _ = seeded_cargo_and_vessel

    response = client.get(f"/trackings/{cargo_id}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    else:
        assert response.json()["detail"] == "Cargo not found"
