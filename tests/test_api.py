import pytest

@pytest.fixture(scope="module", autouse=True)
def setup_initial_data(client):
    # Create contract and extract cargo ID
    contract_response = client.post("/contracts/", json={
        "client_name": "NavegaTech",
        "cargo_type": "Equipamento Marítimo",
        "origin": "Porto",
        "destination": "Rotterdam",
        "price": 15000.00
    })
    assert contract_response.status_code == 200

    # Create vessel
    vessel_response = client.post("/vessels/", json={
        "name": "Mar Lusitano",
        "capacity": 1,
        "current_location": "Porto"
    })
    assert vessel_response.status_code == 200

def test_create_contract_creates_cargo(client):
    response = client.post("/contracts/", json={
        "client_name": "NavegaTech",
        "cargo_type": "Equipamento Marítimo",
        "origin": "Porto",
        "destination": "Rotterdam",
        "price": 15000.00
    })
    assert response.status_code == 200
    data = response.json()
    assert data["client_name"] == "NavegaTech"
    assert data["cargo"]["status"] == "pending"
    assert data["cargo"]["current_location"] == "Porto"


def test_get_existing_contract(client):
    response = client.get("/contracts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "cargo" in data


def test_get_nonexistent_contract(client):
    response = client.get("/contracts/999")
    assert response.status_code == 404


def test_list_contracts(client):
    response = client.get("/contracts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_vessel(client):
    response = client.post("/vessels/", json={
        "name": "Mar Lusitano",
        "capacity": 2,
        "current_location": "Porto"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mar Lusitano"


def test_get_existing_vessel(client):
    response = client.get("/vessels/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_nonexistent_vessel(client):
    response = client.get("/vessels/999")
    assert response.status_code == 404


def test_list_vessels(client):
    response = client.get("/vessels/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_move_vessel_to_pickup_cargo(client):
    # Pickup at Porto
    response = client.post("/vessels/1/move", params={"location": "Porto"})
    assert response.status_code == 200

    # Confirm cargo status is now in transit
    cargo_response = client.get("/cargoes/1")
    assert cargo_response.status_code == 200
    assert cargo_response.json()["status"] == "in_transit"


def test_move_vessel_to_deliver_cargo(client):
    # Move to Rotterdam for delivery
    response = client.post("/vessels/1/move", params={"location": "Rotterdam"})
    assert response.status_code == 200

    # Confirm cargo is now delivered
    cargo_response = client.get("/cargoes/1")
    assert cargo_response.status_code == 200
    assert cargo_response.json()["status"] == "delivered"


def test_get_existing_cargo(client):
    response = client.get("/cargoes/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["pending", "in_transit", "delivered"]


def test_get_nonexistent_cargo(client):
    response = client.get("/cargoes/999")
    assert response.status_code == 404


def test_list_cargoes(client):
    response = client.get("/cargoes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tracking_history(client):
    response = client.get("/trackings/1")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) >= 2  # Porto and Rotterdam
    assert all("location" in entry for entry in history)
