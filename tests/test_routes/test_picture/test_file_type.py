import io

from flask.testing import FlaskClient

ALLOWED_IMAGE = (b"fake image data", "test.jpg")
INVALID_IMAGE = (b"not an image", "test.txt")


def test_upload_missing_file(client: FlaskClient, auth_header):
    """Test upload without any file provided"""
    data = {}  # no file
    response = client.post("/upload", headers=auth_header, data=data)
    print(response.json)
    assert response.status_code == 400
    assert response.json["error"] == "No file provided"


def test_upload_invalid_file_extension(client: FlaskClient, auth_header):
    """Test upload with a file with an invalid extension"""
    data = {
        "file": (io.BytesIO(INVALID_IMAGE[0]), INVALID_IMAGE[1]),
        "type": "avatar",
    }
    response = client.post(
        "/upload", headers=auth_header, data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert response.json["error"] == "Invalid file"


def test_upload_invalid_picture_type(client: FlaskClient, auth_header):
    """Test upload with an invalid picture type"""
    data = {
        "file": (io.BytesIO(ALLOWED_IMAGE[0]), ALLOWED_IMAGE[1]),
        "type": "unknown_type",
    }
    response = client.post(
        "/upload", headers=auth_header, data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert response.json["error"].startswith("Invalid picture type")


def test_upload_missing_authorization(client: FlaskClient):
    """Test upload without the Authorization header"""
    data = {
        "file": (io.BytesIO(ALLOWED_IMAGE[0]), ALLOWED_IMAGE[1]),
        "type": "avatar",
    }
    response = client.post("/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 401
    assert response.json["message"] == "Token is missing or improperly formatted"


def test_upload_file_path_traversal(client: FlaskClient, monkeypatch, auth_header):
    """Simulate a directory traversal attack or path validation failure"""

    def mock_abspath(path):
        return "/etc/passwd"  # outside the allowed folder

    monkeypatch.setattr("os.path.abspath", mock_abspath)

    data = {
        "file": (io.BytesIO(ALLOWED_IMAGE[0]), ALLOWED_IMAGE[1]),
        "type": "avatar",
    }

    response = client.post(
        "/upload", headers=auth_header, data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 400
    assert response.json["error"] == "Invalid file path"
