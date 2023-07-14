import os

from minio import Minio

MINIO_HOSTNAME=os.getenv("MINIO_HOSTNAME")
MINIO_PORT=os.getenv("MINIO_PORT")
MINIO_ENDPOINT = f"{MINIO_HOSTNAME}:{MINIO_PORT}"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_IS_SECURE = os.getenv("MINIO_IS_SECURE")

storage = Minio(
    endpoint=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    # accepts capitalization variants as in FALSE, False and false
    secure=MINIO_IS_SECURE.lower() in ["true"],
)
