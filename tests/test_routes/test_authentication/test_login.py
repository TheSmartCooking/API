from flask.testing import FlaskClient


def test_missing_email(client: FlaskClient, sample_password):
    """Test login with missing email"""
    data = {
        "email": "",  # Missing email
        "password": sample_password,
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"


def test_missing_password(client: FlaskClient, sample_email):
    """Test login with missing password"""
    data = {
        "email": sample_email,
        "password": "",  # Missing password
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"
