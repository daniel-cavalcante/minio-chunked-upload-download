import os

from minio import Minio


MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT") or "localhost:9000"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY") or "minioadmin"
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY") or "minioadmin"
MINIO_IS_SECURE = os.getenv("MINIO_IS_SECURE") or "False"

storage = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    # accepts capitalization variants as in FALSE, False and false
    secure=MINIO_IS_SECURE.lower() in ["true"],
)
