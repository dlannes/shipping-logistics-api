import pytest


@pytest.fixture(scope="module")
def seeded_contract_and_cargo(client):
    response = client.post(
        "/contracts/",
        json={
            "client_name": "PortoLog",
            "cargo_type": "Vinho do Porto",
            "origin": "Porto",
            "destination": "Rotterdam",
            "price": 5000.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    cargo_id = data["cargo"]["id"]
    return cargo_id


def test_list_cargoes_returns_list(client, seeded_contract_and_cargo):
    response = client.get("/cargoes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(cargo["id"] == seeded_contract_and_cargo for cargo in data)


def test_get_existing_cargo_returns_details(client, seeded_contract_and_cargo):
    response = client.get(f"/cargoes/{seeded_contract_and_cargo}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == seeded_contract_and_cargo
    assert data["status"] == "pending"
    assert data["current_location"] == "Porto"


def test_get_nonexistent_cargo_returns_404(client):
    response = client.get("/cargoes/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cargo not found"
