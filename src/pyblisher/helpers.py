import os
from datetime import datetime

from tqdm import tqdm

from .types import (
    ExternalSource,
    InternalSource,
    SourceProperty,
)


############## Dacite Type-Hooks ##############
def parse_datetime(value: str) -> datetime:
    """
    Type-hook for dacite to parse datetime from isoformat.
    It replaces the 'Z' with '+00:00' to make it compatible with fromisoformat.

    :param value: datetime in isoformat
    :type value: str
    :return: datetime
    :rtype: datetime
    """
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def parse_source_property(value: dict) -> SourceProperty:
    """
    Type-hook for dacite to parse SourceProperty from dict.

    :param value: SourceProperty as dict
    :type value: dict
    :return: SourceProperty
    :rtype: SourceProperty
    """
    if value['type'] == 'external':
        return ExternalSource(**value)
    elif value['type'] == 'internal':
        return InternalSource(**value)
    else:
        raise ValueError(f'Unknown SourceProperty type: {value["type"]}')


############## other ##############
def file_upload_generator(filepath: str):
    """
    Generator to upload a file with progress bar.

    :yield: file-like object
    :rtype: file-like object
    """
    total = os.path.getsize(filepath)
    with tqdm(
        ascii=True, unit_scale=True, unit='B', unit_divisor=1024, total=total
    ) as bar:
        with open(filepath, 'rb') as file:
            while chunk := file.read(1024):
                bar.update(len(chunk))
                yield chunk
