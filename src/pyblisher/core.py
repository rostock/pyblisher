from dacite import from_dict
from httpx import Response

from .client import client
from .exceptions import (
    AuthenticationError,
    InternalServerError,
    MatchFailed,
    ObjectNotFound,
    PermissionError,
)
from .Project import Project
from .Settings import settings
from .types import ApiClientProtocol
from .User import User


def get_project(id: str) -> Project:
    """Get project by id.

    Args:
        id: The project id.

    Returns:
        The requested project.

    Raises:
        MatchFailed: If the request parameters are invalid (400).
        AuthenticationError: If authentication fails (401).
        PermissionError: If permission is denied (403).
        ObjectNotFound: If the project is not found (404).
        InternalServerError: If an internal server error occurs (500).
    """
    api: ApiClientProtocol = client
    response: Response = api.get(
        endpoint=f'project/{id}/',
    )
    match response.status_code:
        case 200:
            return from_dict(
                data_class=Project,
                data=response.json(),
                config=settings.dacite_config,
            )
        case 400:
            raise MatchFailed(
                f'{response.status_code} - {response.json()["reason"]}'
            )
        case 401:
            raise AuthenticationError(
                f'{response.status_code} - {response.json()["reason"]}'
            )
        case 403:
            raise PermissionError(
                f'{response.status_code} - {response.json()["reason"]}'
            )
        case 404:
            raise ObjectNotFound(
                f'{response.status_code} - {response.json()["reason"]}'
            )
        case 500:
            raise InternalServerError(
                f'{response.status_code} - {response.json()["reason"]}'
            )
        case _:
            raise Exception(f'Failed to get project. Response: {response}')


def get_user(user_id: str) -> User:
    """Get user by id.

    Args:
        user_id: The user id.

    Returns:
        The requested user.

    Raises:
        Exception: If the request fails.
    """
    api: ApiClientProtocol = client
    response: Response = api.get(
        endpoint=f'user/{user_id}/',
    )
    match response.status_code:
        case 200:
            return from_dict(
                data_class=User,
                data=response.json(),
                config=settings.dacite_config,
            )
        case _:
            raise Exception(f'Failed to get user. Response: {response}')
