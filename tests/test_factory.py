def test_index(client):
    response = client.get('/')
    assert response.data == b"<a href='/minio'>MinIO</a>"
