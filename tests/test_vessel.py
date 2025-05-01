import pytest


@pytest.fixture()
def created_vessel(client):
    response = client.post(
        "/vessels",
        json={"name": "Mar Lusitano", "capacity": 2, "current_location": "Porto"},
    )
    assert response.status_code == 200
    vessel_id = response.json()["id"]
    return vessel_id


def test_create_vessel(client):
    response = client.post(
        "/vessels",
        json={"name": "Navio Atlântico", "capacity": 3, "current_location": "Hamburgo"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Navio Atlântico"
    assert data["capacity"] == 3
    assert data["current_location"] == "Hamburgo"


def test_create_vessel_invalid_input(client):
    response = client.post(
        "/vessels",
        json={
            "name": "",
            "capacity": "large",
            "current_location": "Lisboa",
        },
    )
    assert response.status_code == 422


def test_move_existing_vessel(client, created_vessel):
    response = client.post(
        f"/vessels/{created_vessel}/move", params={"location": "Rotterdam"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["current_location"] == "Rotterdam"


def test_move_nonexistent_vessel(client):
    response = client.post("/vessels/9999/move", params={"location": "Valencia"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Vessel not found"


def test_get_existing_vessel(client, created_vessel):
    response = client.get(f"/vessels/{created_vessel}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_vessel
    assert "name" in data
    assert "capacity" in data


def test_get_nonexistent_vessel(client):
    response = client.get("/vessels/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Vessel not found"


def test_list_vessels(client, created_vessel):
    response = client.get("/vessels")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(vessel["id"] == created_vessel for vessel in data)
