from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional, Union

from dacite import from_dict
from httpx import Response

from .Bucket import Bucket
from .client import client
from .exceptions import AuthenticationError, ObjectNotFound
from .Settings import settings
from .Source import Source
from .Task import Task
from .types import (
    ApiClientProtocol,
    ExternalSource,
    InternalSource,
    Schedule,
)


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
    _api: ApiClientProtocol = field(default=client, init=False, repr=False)
    _endpoint: str = field(init=False, repr=False)

    # required api attributes
    _id: str
    name: str
    bbox: list[float]
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
            json=data,
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
    def create_source(
        self,
        name: str,
        sourceProperties: Union[InternalSource, ExternalSource],
        type: Literal[
            'tileset',
            'tilesetupdate',
            'geojson',
            'oblique',
            'qmesh',
            'meshinmesh',
            'wms',
            'wmts',
            'tms',
            'vectortiles',
            'generic',
        ],
        typeProperties: dict = {},
        description: Optional[str] = None,
        bbox: Optional[list] = None,
        properties: Optional[dict] = None,
    ):
        """
        Create a datasource for this project.

        :param name: datasource name
        :type name: str
        :param sourceProperties: bucket info
        :type sourceProperties: InternalSource | ExternalSource
        :param type: datasource type (e.g. 'tileset', 'geojson', 'wms', etc.)
        :type type: str
        :param typeProperties: datasource type properties
        :type typeProperties: dict
        :param description: optional datasource description
        :type description: str
        :param bbox: optional bounding box
        :type bbox: list
        :param properties: optional datasource properties
        :type properties: dict
        :return: new datasource
        :rtype: Source
        """
        # prepare post request data
        data = {
            'name': name,
            'sourceProperties': sourceProperties,
            'type': type,
            'typeProperties': typeProperties,
        }
        # add optional parameters
        if description:
            data['description'] = description
        if bbox:
            data['bbox'] = bbox
        if properties:
            data['properties'] = properties

        # send post request
        response: Response = self._api.post(
            endpoint=self._endpoint + 'datasource/',
            json=data,
        )
        # validate response
        match response.status_code:
            case 201:
                return from_dict(
                    data_class=Source,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 401:
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:
                raise Exception(
                    f'Failed to create datasource. Response: {response.__dict__}'
                )

    def get_source(self, id: str):
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

    def get_sources(self):
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
    def create_task(
        self,
        name: str,
        parameters: dict,
        jobType: str,
        schedule: Schedule,
        labels: Optional[list[str]] = None,
        tags: Optional[dict] = None,
        debugLevel: Optional[int] = None,  # 0-2
        priority: Optional[float] = None,
        description: Optional[str] = None,
        properties: Optional[dict] = None,
        jobVersion: Optional[str] = None,
    ):
        """
        Create a task for this project.
        """
        # prepare post request data
        data = {
            'name': name,
            'parameters': parameters,
            'jobType': jobType,
            'schedule': schedule.__dict__,
        }
        print(data)
        # add optional parameters
        if labels:
            data['labels'] = labels
        if tags:
            data['tags'] = tags
        if debugLevel:
            data['debugLevel'] = debugLevel
        if priority:
            data['priority'] = priority
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties
        if jobVersion:
            data['jobVersion'] = jobVersion

        # send post request
        response = self._api.post(
            endpoint=self._endpoint + 'task/',
            json=data,
        )
        # validate response
        match response.status_code:
            case 201:
                return from_dict(
                    data_class=Task,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 401:
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:
                raise Exception(
                    f'Failed to create task. Response: {response.__dict__}'
                )

    def get_task(self, id: str):
        """
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

    ############## Test Methods ##############
    def test_task_create(self):
        """
        Test the create_task method.
        """
        task = self.create_task(
            name='Crazy Task name',
            parameters={
                'command': 'conversion',
                'epsgCode': 25833,
                'datasource': {
                    'command': 'update',
                    'datasourceId': '1e78b0ab-1445-4e15-8d34-6d0eacf15889',
                },
                'dataset': {
                    'type': 'internal',
                    'dataBucketId': '287a24ab-a3bf-4d68-9d31-dfbd35ebdd46',
                    'dataBucketKey': '/',
                },
            },
            jobType='pointcloud',
            schedule=ImmediateSchedule(type='immediate'),
        )
        return task
