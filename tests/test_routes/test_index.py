from app import app


def test_index_route():
    response = app.test_client().get("/")
    expected_response = '{"data":{"message":"Hello there!"},"success":true}'

    assert response.status_code == 200
    assert response.data.decode("utf-8").strip() == expected_response
