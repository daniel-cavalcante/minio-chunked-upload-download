import os
from typing import Any

from minio import Minio

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE") or 10 * 1024 * 1024)


def upload_to_storage(
    storage: Minio, bucket_name: str, object_name: str, data: Any
) -> bool:
    try:
        if not storage.bucket_exists(bucket_name):
            storage.make_bucket(bucket_name)
        result = storage.put_object(
            bucket_name, object_name,
            data.stream, length=-1, part_size=CHUNK_SIZE
        )
    except Exception:
        raise
    else:
        return True if result else False


def get_chunk_number(name: str) -> int:
    """Get the chunk number from the chunk's file name string.

    Example:
        >>> name="file_name.ext.chunk1of8"
        >>> x=name.split('.chunk')
        >>> x
        ['file_name.ext', '1of8']
        >>> y=x[-1].split('of')
        >>> y
        ['1', '8']
        >>> int(y[0], base=10)
        1
    """
    x = name.split(".chunk")
    y = x[-1].split("of")
    return int(y[0], base=10)


def list_objects(storage: Minio, bucket_name) -> list[str]:
    object_list = []
    for item in storage.list_objects(bucket_name, recursive=True):
        object_list.append(item.object_name)
    object_list.sort(key=get_chunk_number)
    return object_list


def get_filename(storage: Minio, bucket_name):
    object_list = list_objects(storage, bucket_name)
    # similar to function get_chunk_number but it takes the file name
    return object_list[0].split(".chunk")[0]


def get_file_chunks(storage: Minio, bucket_name):
    object_list = list_objects(storage, bucket_name)
    for object_name in object_list:
        chunk = storage.get_object(bucket_name, object_name)
        if chunk is None:
            break
        yield chunk.read(CHUNK_SIZE)
