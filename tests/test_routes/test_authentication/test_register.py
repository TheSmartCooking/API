from flask.testing import FlaskClient


def test_missing_email(client: FlaskClient, sample_username, sample_password):
    """Test registration with missing email"""
    data = {
        "username": sample_username,
        "email": "",  # Missing email
        "password": sample_password,
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Username, email, and password are required"


def test_missing_password(client: FlaskClient, sample_username, sample_email):
    """Test registration with missing password"""
    data = {
        "username": sample_username,
        "email": sample_email,
        "password": "",  # Missing password
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Username, email, and password are required"


def test_missing_username(client: FlaskClient, sample_username, sample_email):
    """Test registration with missing username"""
    data = {
        "username": sample_username,  # Missing username
        "email": sample_email,
        "password": "",  # Missing password
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Username, email, and password are required"


def test_invalid_email(client: FlaskClient, sample_username, sample_password):
    """Test registration with an invalid email format"""
    data = {
        "username": sample_username,
        "email": "invalid-email",  # Invalid email format
        "password": sample_password,
    }
    response = client.post("/register", json=data)

    assert response.status_code == 400
    assert response.json["message"] == "Invalid email address"
