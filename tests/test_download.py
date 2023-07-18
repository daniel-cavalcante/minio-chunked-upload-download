from dataclasses import dataclass
from source.storage import storage


@dataclass()
class MockBucket:
    name: str


def test_download_route(client, monkeypatch):
    def mock_list():
        return [MockBucket("bucket1"), MockBucket("bucket2")]

    monkeypatch.setattr(storage, "list_buckets", mock_list)

    response = client.get("/minio/download")
    assert response.data == b'["bucket1","bucket2"]\n'
