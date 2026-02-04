import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

# from src.database import Base, engine
from src.main import app

# -------------------------------------------------------------------
# Database setup / teardown (SQLite-safe)
# -------------------------------------------------------------------


# @pytest.fixture(scope="session", autouse=True)
# def setup_database():
#     """
#     Create all tables for SQLite before tests.
#     Drop them after the test session.
#     """
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """
    FastAPI test client (function-scoped for safety).
    """
    return TestClient(app)


# -------------------------------------------------------------------
# Patient tests
# -------------------------------------------------------------------


def test_create_patient(client):
    email = f"test_{uuid.uuid4()}@example.com"

    response = client.post(
        "/patients",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "phone": "9999999999",
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == email


def test_duplicate_patient_email(client):
    unique_email = f"test_{uuid.uuid4()}@example.com"

    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": unique_email,
        "phone": "9999999999",
    }

    r1 = client.post("/patients", json=payload)
    assert r1.status_code == 201

    r2 = client.post("/patients", json=payload)
    assert r2.status_code == 409


# -------------------------------------------------------------------
# Doctor tests
# -------------------------------------------------------------------


def test_create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "full_name": "Dr John Doe",
            "specialization": "Cardiology",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["full_name"] == "Dr John Doe"
    assert data["specialization"] == "Cardiology"
    assert data["is_active"] is True


def test_get_doctor_not_found(client):
    response = client.get("/doctors/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"


# -------------------------------------------------------------------
# Appointment tests
# -------------------------------------------------------------------


def test_create_appointment(client):
    doctor = client.post(
        "/doctors",
        json={"full_name": "Dr Test", "specialization": "General"},
    ).json()

    patient = client.post(
        "/patients",
        json={
            "first_name": "Appt",
            "last_name": "User",
            "email": f"appt_{uuid.uuid4()}@example.com",
            "phone": "8888888888",
        },
    ).json()

    start_time = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "start_time": start_time,
            "duration_minutes": 30,
        },
    )

    assert response.status_code == 201


def test_overlapping_appointment(client):
    doctor = client.post(
        "/doctors",
        json={"full_name": "Dr Overlap", "specialization": "General"},
    ).json()

    patient = client.post(
        "/patients",
        json={
            "first_name": "Overlap",
            "last_name": "User",
            "email": f"overlap_{uuid.uuid4()}@example.com",
            "phone": "7777777777",
        },
    ).json()

    base_time = datetime.now(timezone.utc) + timedelta(hours=3)

    r1 = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "start_time": base_time.isoformat(),
            "duration_minutes": 30,
        },
    )
    assert r1.status_code == 201

    r2 = client.post(
        "/appointments",
        json={
            "patient_id": patient["id"],
            "doctor_id": doctor["id"],
            "start_time": (base_time + timedelta(minutes=15)).isoformat(),
            "duration_minutes": 30,
        },
    )
    assert r2.status_code == 409
