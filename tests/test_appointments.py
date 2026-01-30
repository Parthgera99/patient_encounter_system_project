import uuid
from datetime import datetime, timedelta, timezone


def test_create_appointment(client):
    # create doctor
    doctor = client.post(
        "/doctors",
        json={"full_name": "Dr Test", "specialization": "General"},
    ).json()

    # create patient
    patient = client.post(
        "/patients",
        json={
            "first_name": "Appt",
            "last_name": "User",
            "email": f"test_{uuid.uuid4()}@example.com",
            "phone": "8888888888",
        },
    ).json()

    start_time = (
        datetime.now(timezone.utc) + timedelta(hours=2)
    ).isoformat()

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


def test_duplicate_appointment(client):
    start_time = (
        datetime.now(timezone.utc) + timedelta(hours=2)
    ).isoformat()

    response = client.post(
        "/appointments",
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "start_time": start_time,
            "duration_minutes": 30,
        },
    )

    # first one may or may not exist, second must fail
    response2 = client.post(
        "/appointments",
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "start_time": start_time,
            "duration_minutes": 30,
        },
    )

    assert response2.status_code == 409
