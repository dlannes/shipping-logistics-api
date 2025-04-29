import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from app.main import get_db
from app.main import app

# Set up test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Ensure clean slate
if os.path.exists("test.db"):
    os.remove("test.db")

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Run Alembic migrations for test DB
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

run_migrations()

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test client fixture
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
