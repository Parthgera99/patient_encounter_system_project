import uuid


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
    data = response.json()
    assert data["email"] == email


def test_duplicate_patient_email(client):
    response = client.post(
        "/patients",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test_user_001@example.com",
            "phone": "9999999999",
        },
    )

    assert response.status_code == 409
