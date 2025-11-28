import os
from datetime import datetime

from tqdm import tqdm

from .types import ExternalSource, InternalSource, SourceProperty


############## Dacite Type-Hooks ##############
def parse_datetime(value: str) -> datetime:
    """Parse datetime from isoformat string.

    Type-hook for dacite to parse datetime from isoformat.
    It replaces the 'Z' with '+00:00' to make it compatible with fromisoformat.

    Args:
        value: Datetime in isoformat.

    Returns:
        Parsed datetime object.
    """
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def parse_source_property(value: dict) -> SourceProperty:
    """Parse SourceProperty from dict.

    Type-hook for dacite to parse SourceProperty from dict.

    Args:
        value: SourceProperty as dict.

    Returns:
        Parsed SourceProperty object (ExternalSource or InternalSource).

    Raises:
        ValueError: If the SourceProperty type is unknown.
    """
    if value['type'] == 'external':
        return ExternalSource(**value)
    elif value['type'] == 'internal':
        return InternalSource(**value)
    else:
        raise ValueError(f'Unknown SourceProperty type: {value["type"]}')


############## other ##############
def file_upload_generator(filepath: str):
    """Generate file chunks for upload with progress bar.

    Generator to upload a file with progress bar.

    Args:
        filepath: Path to the file to upload.

    Yields:
        File chunks of 1024 bytes.
    """
    total = os.path.getsize(filepath)
    with tqdm(
        ascii=True, unit_scale=True, unit='B', unit_divisor=1024, total=total
    ) as bar:
        with open(filepath, 'rb') as file:
            while chunk := file.read(1024):
                bar.update(len(chunk))
                yield chunk
