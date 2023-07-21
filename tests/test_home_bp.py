def test_index(client):
    response = client.get("/")
    assert response.data == b"<a href='/minio'>MinIO</a>"
    assert response.status_code == 200
