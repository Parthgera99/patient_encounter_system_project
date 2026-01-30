import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from src.patient_encounter_system.database import engine
from src.patient_encounter_system.main import app


@pytest.fixture(scope="session", autouse=True)
def cleanup_tables():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM parthAppointments"))
        conn.execute(text("DELETE FROM parthPatients"))
        conn.execute(text("DELETE FROM parthDoctors"))


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
