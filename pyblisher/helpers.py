from datetime import datetime


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
