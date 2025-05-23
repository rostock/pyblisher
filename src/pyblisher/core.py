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
    """
    Get project by id

    :param project_id: project id
    :type project_id: str
    :return: project
    :rtype: Project
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
    """
    Get user by id

    :param user_id: user id
    :type user_id: str
    :return: user
    :rtype: User
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
