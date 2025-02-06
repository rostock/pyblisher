from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from dacite import from_dict
from httpx import Response

from .Bucket import Bucket
from .client import ApiClient
from .exceptions import AuthenticationError, ObjectNotFound
from .Settings import settings
from .Source import Source
from .Task import Task


@dataclass
class Project:
    """
    This class implements the structure of Projects of the VC Publisher API.

    :attribute _id: project id
    :atype _id: str
    :attribute name: project name
    :atype name: str
    :attribute bbox: project bounding box
    :atype bbox: list
    :attribute defaultDataBucketId: default data bucket id
    :atype defaultDataBucketId: str
    :attribute createdAt: project creation date
    :atype createdAt: datetime
    :attribute updatedAt: project update date
    :atype updatedAt: datetime
    :attribute createdBy: project creator
    :atype createdBy: User
    :attribute updatedBy: project last updater
    :atype updatedBy: User
    :attribute description: project description
    :atype description: str
    :attribute properties: project properties
    :atype properties: dict
    """

    # Internal attributes
    _api: ApiClient = field(default=ApiClient(), init=False, repr=False)
    _endpoint: str = field(init=False, repr=False)

    # required api attributes
    _id: str
    name: str
    bbox: list
    defaultDataBucketId: str  # TODO: converted automatically to Bucket
    createdAt: datetime
    updatedAt: datetime
    createdBy: str | None
    updatedBy: str

    # optional api attributes
    description: Optional[str]
    properties: Optional[dict]

    ############## Data-Buckets ##############
    def create_bucket(
        self,
        name: str,
        description: Optional[str] = None,
        properties: Optional[dict] = None,
    ) -> Bucket:
        """
        Create a bucket for this project.

        :param name: bucket name
        :type name: str
        :param description: optional bucket description
        :type description: str
        :param properties: optional bucket properties
        :type properties: dict
        :return: new bucket
        :rtype: Bucket
        """
        # prepare post request data
        data: dict = {'name': name}
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties

        # send post request
        response = self._api.post(
            endpoint=self._endpoint + 'data-bucket/',
            data=data,
        )
        # validate response
        match response.status_code:
            case 201:  # Created
                return from_dict(
                    data_class=Bucket,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:  # All other cases
                raise Exception(
                    f'Failed to create bucket. Response: {response.__dict__}'
                )

    def get_bucket(self, id: str) -> Bucket:
        """
        Get a bucket for this project.

        :param id: bucket id
        :type id: str
        :return: bucket
        :rtype: Bucket
        """
        response = self._api.get(endpoint=self._endpoint + f'data-bucket/{id}/')
        match response.status_code:
            case 200:  # OK
                return from_dict(
                    data_class=Bucket,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 404:  # Not found
                raise ObjectNotFound(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:  # All other cases
                raise Exception(
                    f'Failed to get bucket. Response: {response.__dict__}'
                )

    def get_buckets(self) -> list[Bucket]:
        """
        Get all buckets for this project.

        :return: list of buckets
        :rtype: list
        """
        response = self._api.get(endpoint=self._endpoint + 'data-buckets/')
        match response.status_code:
            case 200:  # OK
                content = response.json()
                return [
                    from_dict(
                        data_class=Bucket,
                        data=bucket,
                        config=settings.dacite_config,
                    )
                    for bucket in content['items']
                ]
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 404:  # Not found
                raise ObjectNotFound(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:  # All other cases
                raise Exception(
                    f'Failed to get buckets. Response: {response.__dict__}'
                )

    ############## Datasources ##############
    def create_datasource(self, name: str, description: str):
        """
        Not implemented yet.
        Create a datasource for this project.
        """
        pass

    def get_datasource(self, id: str):
        """
        Get a datasource for this project.
        """
        response: Response = self._api.get(
            endpoint=self._endpoint + f'datasource/{id}/',
        )
        match response.status_code:
            case 200:
                return from_dict(
                    data_class=Source,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 401:
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 404:
                raise ObjectNotFound(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:
                raise Exception(
                    f'Failed to get datasource. Response: {response.__dict__}'
                )

    def get_datasources(self):
        """
        Get all datasources for this project.
        """
        response: Response = self._api.get(
            endpoint=self._endpoint + 'datasources/',
        )
        datasources = [
            from_dict(
                data_class=Source,
                data=datasource,
                config=settings.dacite_config,
            )
            for datasource in response.json()['items']
        ]
        return datasources

    ############## Tasks ##############
    def create_task(self, name: str, description: str):
        """
        Not implemented yet.
        Create a task for this project.
        """
        pass

    def get_task(self, id: str):
        """
        Not implemented yet.
        Get a task for this project.
        """
        response: Response = self._api.get(
            endpoint=self._endpoint + f'task/{id}/'
        )
        match response.status_code:
            case 200:
                return from_dict(
                    data_class=Task,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 401:
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 404:
                raise ObjectNotFound(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:
                raise Exception(
                    f'Failed to get task. Response: {response.__dict__}'
                )

    def get_tasks(self):
        """
        Not implemented yet.
        Get all tasks for this project.
        """
        response: Response = self._api.get(endpoint=self._endpoint + 'tasks/')
        tasks = [
            from_dict(
                data_class=Task,
                data=task,
                config=settings.dacite_config,
            )
            for task in response.json()['items']
        ]
        return tasks

    ############## Dunder Methods ##############
    def __post_init__(self):
        """
        Initialize the API endpoint, after the object is created.
        """
        self._endpoint = f'project/{self._id}/'

    def __str__(self):
        """
        String representation of the object as its id.
        """
        return self._id
