from uuid import uuid4

from sqlalchemy import UUID, Column, String
from source.database import db


class BucketObject(db.Model):
    __tablename__ = "bucket_object"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    bucket_name = Column(String, nullable=False, comment="Bucket name")
    filename = Column(String, nullable=False, comment="Video object name in minio")
