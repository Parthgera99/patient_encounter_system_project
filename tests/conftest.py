import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from src.database import engine
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def cleanup_tables():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM parthGeraAppointments"))
        conn.execute(text("DELETE FROM parthGeraPatients"))
        conn.execute(text("DELETE FROM parthGeraDoctors"))


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
