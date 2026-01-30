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
