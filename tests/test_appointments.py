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
    # create doctor
    doctor = client.post(
        "/doctors",
        json={"full_name": "Dr Overlap", "specialization": "General"},
    ).json()

    # create patient
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

    # first appointment: 10:00–10:30
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

    # second appointment: 10:15–10:45 (OVERLAPS)
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
