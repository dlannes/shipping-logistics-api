import pytest


@pytest.fixture(scope="module")
def created_contract(client):
    response = client.post(
        "/contracts",
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
    contract_id = data["id"]
    return contract_id


def test_create_contract(client):
    response = client.post(
        "/contracts",
        json={
            "client_name": "NavalCo",
            "cargo_type": "Peças Industriais",
            "origin": "Porto",
            "destination": "Hamburgo",
            "price": 10000.0,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["client_name"] == "NavalCo"
    assert data["origin"] == "Porto"
    assert data["destination"] == "Hamburgo"
    assert data["price"] == 10000.0
    assert data["cargo"]["status"] == "pending"


def test_get_existing_contract(client, created_contract):
    response = client.get(f"/contracts/{created_contract}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_contract
    assert "cargo" in data


def test_get_nonexistent_contract(client):
    response = client.get("/contracts/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contract not found"


def test_list_contracts(client, created_contract):
    response = client.get("/contracts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(contract["id"] == created_contract for contract in data)
