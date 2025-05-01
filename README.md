# Shipping Logistics API

An API for managing a logistics company that ships general goods via vessels.

It tracks:
- **Contracts**: agreements with clients for cargo shipments.
- **Cargoes**: goods linked to each contract, automatically created.
- **Vessels**: ships that pick up and deliver cargo between ports.
- **Tracking**: historical log of cargo movements over time.

---

## Setup Instructions

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:

- Using pip:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-dev.txt  # For development dependencies
    ```

- Using pip-tools:
    ```bash
    pip install pip-tools
    pip-sync requirements.txt requirements-dev.txt
    ```

- Using poetry:
    ```bash
    poetry install --with dev
    ```

3. **Apply database migrations** (using Alembic):

    ```bash
    alembic upgrade head
    ```

4. **Run the application**:

    ```bash
    uvicorn app.main:app --reload
    ```

---

## API Documentation

Base URL: `/`

### **Contracts**

- `POST /contracts`
    - Create a new shipping contract (auto-creates cargo).
    - Input:
        ```json
        {
            "client_name": "string",
            "cargo_type": "string",
            "origin": "string",
            "destination": "string",
            "price": float
        }
        ```
    - Output:
        - Contract object, including a linked cargo (with status `"pending"`).

- `GET /contracts/{contract_id}`
    - Retrieve contract by ID.

- `GET /contracts`
    - List all contracts.

---

### **Cargoes**

- `GET /cargoes/{cargo_id}`
    - Retrieve cargo details by ID.

- `GET /cargoes`
    - List all cargoes.

---

### **Vessels**

- `POST /vessels`
    - Register a new vessel.
    - Input:
        ```json
        {
            "name": "string",
            "capacity": int,
            "current_location": "string"
        }
        ```
    - Output:
        - Vessel object.

- `POST /vessels/{vessel_id}/move?location=NewLocation`
    - Update vessel location.
    - Behavior:
        - If at the origin of a pending cargo and has space, picks up cargo.
        - If at the destination of an in-transit cargo, delivers cargo.
    - Notes:
        - **Port names must match exactly** for pickup/delivery.
        - **Vessel capacity must allow space** for picking up new cargo.
    - Output:
        - Updated vessel object.

- `GET /vessels/{vessel_id}`
    - Retrieve vessel details by ID.

- `GET /vessels`
    - List all vessels.

---

### **Tracking**

- `GET /trackings/{cargo_id}`
    - Retrieve the full tracking history for a cargo.
    - Output:
        ```json
        [
            { "location": "string", "timestamp": "datetime" },
            ...
        ]
        ```

---

## Design Decisions

- **Contracts + Cargo**:
    - A contract represents a client’s shipping agreement and automatically generates an associated cargo when created.
    - Clients **do not create cargo directly**; the system handles it.

- **Tracking History**:
    - Tracking records are automatically created:
        - When a vessel **picks up** cargo.
        - When a vessel **delivers** cargo.
    - This gives a full movement log over time, without manual tracking entries.

- **Port Matching + Capacity Checks**:
    - For a vessel to pick up cargo:
        - It must be at the **same port** as the cargo’s origin.
        - It must have **remaining capacity**.
    - For a vessel to deliver cargo:
        - It must reach the **cargo’s destination port**.

- **Service Layer**:
    - All business logic (e.g., pickup/delivery handling, capacity checking) is isolated inside service classes.
    - This keeps API routes lightweight and focused only on request/response handling.

---

## Possible Future Improvements

- **Port Registry**:
    - Currently, ports are just free-text names.
    - We could introduce a **Ports system** to formally register available ports, prevent typos, and link vessels + cargo to valid ports.

- **Route Planning**:
    - Right now, vessels can “jump” between ports.
    - A more advanced system would track:
        - Vessel routes.
        - Intermediate ports.
        - Time estimates and scheduling.
    - This would increase realism but also complexity, going beyond this challenge’s scope.

- **Advanced Cargo Management**:
    - In the real world, we would also need:
        - Cargo dimensions and weight (not just unit counts).
        - Compatibility between cargo types and vessel capabilities.
        - Multi-leg shipments.

---

## Package Overview

| Package | Purpose |
|---------|---------|
| **FastAPI** | Web framework for async API development. |
| **SQLAlchemy** | Database ORM and schema modeling. |
| **Alembic** | Database migrations and schema versioning. |
| **Pydantic** | Data validation and API response modeling. |
| **Uvicorn** | ASGI server to run the FastAPI app. |
| **httpx** | HTTP client used for testing. |

**Dev-only tools**:
- **pytest** → testing.
- **black** → code formatting.
- **flake8** → linting.
- **mypy** → static type checking.

---

## Usage Notes

- **Start by creating contracts**.
    - This generates pending cargo.
- **Register vessels** next.
- **Move vessels** between ports:
    - At the cargo’s origin → picks up if space.
    - At the cargo’s destination → delivers.
- **Check tracking** to see the full movement history.

---

## Running Tests

```bash
pytest
```

## Checking Code Style

```bash
black --check .
flake8 .
mypy .
```

---

## Author

Dan Esteve  
dan.lannes@outlook.com