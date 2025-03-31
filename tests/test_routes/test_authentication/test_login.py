from flask.testing import FlaskClient


def test_missing_username(client: FlaskClient, sample_password):
    """Test login with missing username"""
    data = {
        "username": "",  # Missing username
        "password": sample_password,
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"


def test_missing_password(client: FlaskClient, sample_username):
    """Test login with missing password"""
    data = {
        "username": sample_username,
        "password": "",  # Missing password
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Email and password are required"
