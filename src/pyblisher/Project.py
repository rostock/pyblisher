from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Optional

from dacite import from_dict
from httpx import Response

from .Bucket import Bucket
from .client import client
from .exceptions import (
    AuthenticationError,
    InternalServerError,
    MatchFailed,
    ObjectNotFound,
    PermissionError,
)
from .Settings import settings
from .Source import Source
from .Task import Task
from .types import ApiClientProtocol


@dataclass
class Project:
    """Structure of Projects of the VC Publisher API.

    Attributes:
        _id: Project id.
        name: Project name.
        bbox: Project bounding box.
        defaultDataBucketId: Default data bucket id.
        createdAt: Project creation date.
        updatedAt: Project update date.
        createdBy: Project creator.
        updatedBy: Project last updater.
        description: Project description.
        properties: Project properties.
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
        """Create a bucket for this project.

        Args:
            name: Bucket name.
            description: Optional bucket description.
            properties: Optional bucket properties.

        Returns:
            The newly created bucket.

        Raises:
            MatchFailed: If the request parameters are invalid (400).
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            InternalServerError: If an internal server error occurs (500).
        """
        # prepare post request data
        data: dict = {'name': name}
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties

        # send post request
        response = self._api.post(
            endpoint=self._endpoint + 'data-bucket/', json=data
        )
        # validate response
        match response.status_code:
            case 201:  # Created
                return from_dict(
                    data_class=Bucket,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 400:  # Match failed
                raise MatchFailed(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 500:  # Internal server error
                raise InternalServerError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:  # All other cases
                raise Exception(
                    f'Failed to create bucket. Response: {response.__dict__}'
                )

    def get_bucket(self, id: str) -> Bucket:
        """Get a bucket for this project.

        Args:
            id: Bucket id.

        Returns:
            The requested bucket.

        Raises:
            MatchFailed: If the request parameters are invalid (400).
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the bucket is not found (404).
        """
        response = self._api.get(endpoint=self._endpoint + f'data-bucket/{id}/')
        match response.status_code:
            case 200:  # OK
                return from_dict(
                    data_class=Bucket,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 400:  # Match failed
                raise MatchFailed(
                    f'{response.status_code} - {response.json()["reason"]}'
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

    def update_bucket(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        properties: Optional[dict] = None,
    ) -> Bucket:
        """Update a bucket for this project.

        Args:
            id: Bucket id.
            name: Updated bucket name.
            description: Updated bucket description.
            properties: Updated bucket properties.

        Returns:
            The updated bucket.

        Raises:
            MatchFailed: If the request parameters are invalid (400).
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            InternalServerError: If an internal server error occurs (500).
        """
        # prepare put request data
        data: dict[str, Any] = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if properties:
            data['properties'] = properties

        # send put request
        response = self._api.put(
            endpoint=self._endpoint + f'data-bucket/{id}/', json=data
        )
        # validate response
        match response.status_code:
            case 200:  # OK
                return from_dict(
                    data_class=Bucket,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 400:  # Match failed
                raise MatchFailed(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 500:  # Internal server error
                raise InternalServerError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:  # All other cases
                raise Exception(
                    f'Failed to update bucket. Response: {response.__dict__}'
                )

    def get_buckets(self) -> tuple[list[Bucket], int, int, int, int]:
        """Get all buckets for this project.

        Returns:
            A tuple containing:
                - List of buckets.
                - Limit (items per page).
                - Current page number.
                - Total pages.
                - Total count of items.

        Raises:
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the project is not found (404).
        """
        response = self._api.get(endpoint=self._endpoint + 'data-buckets/')
        match response.status_code:
            case 200:  # OK
                data = response.json()
                buckets = [
                    from_dict(
                        data_class=Bucket,
                        data=bucket,
                        config=settings.dacite_config,
                    )
                    for bucket in data['items']
                ]
                limit = data['limit']
                page = data['page']
                totalPages = data['totalPages']
                totalCount = data['totalCount']
                return buckets, limit, page, totalPages, totalCount
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
        sourceProperties: dict,  # Union[InternalSource, ExternalSource],
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
    ) -> Source:
        """Create a datasource for this project.

        Args:
            name: Datasource name.
            sourceProperties: Bucket info (InternalSource or ExternalSource).
            type: Datasource type (e.g. 'tileset', 'geojson', 'wms', etc.).
            typeProperties: Datasource type properties.
            description: Optional datasource description.
            bbox: Optional bounding box.
            properties: Optional datasource properties.

        Returns:
            The newly created datasource.

        Raises:
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
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
            endpoint=self._endpoint + 'datasource/', json=data
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

    def get_source(self, id: str) -> Source:
        """Get a datasource for this project.

        Args:
            id: Datasource id.

        Returns:
            The requested datasource.

        Raises:
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the datasource is not found (404).
        """
        response: Response = self._api.get(
            endpoint=self._endpoint + f'datasource/{id}/'
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

    def update_source(
        self,
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        bbox: Optional[list] = None,
        properties: Optional[dict] = None,
        typeProperties: Optional[dict] = None,
        sourceProperties: Optional[dict] = None,
        overwriteParameters: Optional[bool] = False,
    ) -> Source:
        """Update a datasource's attributes.

        Args:
            id: Datasource id.
            name: Updated datasource name.
            description: Updated datasource description.
            bbox: Updated bounding box.
            properties: Updated datasource properties.
            typeProperties: Updated type properties.
            sourceProperties: Updated source properties.
            overwriteParameters: Whether to overwrite parameters. Defaults to False.

        Returns:
            The updated datasource.

        Raises:
            MatchFailed: If the request parameters are invalid (400).
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the datasource is not found (404).
            InternalServerError: If an internal server error occurs (500).
        """
        # prepare put request data
        data: dict[str, Any] = {}
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if bbox:
            data['bbox'] = bbox
        if properties:
            data['properties'] = properties
        if typeProperties:
            data['typeProperties'] = typeProperties
        if sourceProperties:
            data['sourceProperties'] = sourceProperties

        response: Response = self._api.put(
            endpoint=self._endpoint + 'datasource/' + id,
            json=data,
        )
        match response.status_code:
            case 200:  # OK
                return from_dict(
                    data_class=Source,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 400:  # Match failed
                raise MatchFailed(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 404:  # Object not Found
                raise ObjectNotFound(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 500:  # Internal server error
                raise InternalServerError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:
                raise Exception(
                    f'Unexpected status code - {response.status_code}: {response.__dict__}'
                )

    def get_sources(self) -> tuple[list[Source], int, int, int, int]:
        """Get all datasources for this project.

        Returns:
            A tuple containing:
                - List of datasources.
                - Limit (items per page).
                - Current page number.
                - Total pages.
                - Total count of items.

        Raises:
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the project is not found (404).
        """
        response: Response = self._api.get(
            endpoint=self._endpoint + 'datasources/'
        )
        match response.status_code:
            case 200:  # OK
                data = response.json()
                datasources: list[Source] = [
                    from_dict(
                        data_class=Source,
                        data=datasource,
                        config=settings.dacite_config,
                    )
                    for datasource in data['items']
                ]
                limit: int = data['limit']
                page: int = data['page']
                totalPages: int = data['totalPages']
                totalCount: int = data['totalCount']
                return datasources, limit, page, totalPages, totalCount
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

    ############## Tasks ##############
    def create_task(
        self,
        name: str,
        parameters: dict,
        jobType: str,
        schedule: dict,
        labels: Optional[list[str]] = None,
        tags: Optional[dict] = None,
        debugLevel: Optional[int] = None,  # 0-2
        priority: Optional[float] = None,
        description: Optional[str] = None,
        properties: Optional[dict] = None,
        jobVersion: Optional[str] = None,
    ) -> Task:
        """Create a task for this project.

        Args:
            name: Task name.
            parameters: Task parameters.
            jobType: Task job type.
            schedule: Task schedule configuration.
            labels: Optional task labels.
            tags: Optional task tags.
            debugLevel: Optional task debug level (0-2).
            priority: Optional task priority.
            description: Optional task description.
            properties: Optional task properties.
            jobVersion: Optional task job version.

        Returns:
            The newly created task.

        Raises:
            MatchFailed: If the request parameters are invalid (400).
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            InternalServerError: If an internal server error occurs (500).
        """
        # prepare post request data
        data: dict[str, Any] = {
            'name': name,
            'parameters': parameters,
            'jobType': jobType,
            'schedule': schedule,
        }
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
        response = self._api.post(endpoint=self._endpoint + 'task/', json=data)
        # validate response
        match response.status_code:
            case 200:  # OK
                return from_dict(
                    data_class=Task,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 201:  # Created
                return from_dict(
                    data_class=Task,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 400:  # Match failed
                raise MatchFailed(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 500:  # Internal server error
                raise InternalServerError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:
                raise Exception(
                    f'Failed to create task. Response: {response.__dict__}'
                )

    def get_task(self, id: str) -> Task:
        """Get a task for this project.

        Args:
            id: Task id.

        Returns:
            The requested task.

        Raises:
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the task is not found (404).
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

    def update_task(
        self,
        id: str,
        labels: Optional[list] = None,
        tags: Optional[dict] = None,
        debugLevel: Optional[int] = None,  # 0-2
        priority: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[dict] = None,
        properties: Optional[dict] = None,
        schedule: Optional[dict] = None,
        overwriteParameters: Optional[bool] = False,
    ) -> Task:
        """Update a task of this project.

        Args:
            id: Task id.
            labels: Updated task labels.
            tags: Updated task tags.
            debugLevel: Updated task debug level (0-2).
            priority: Updated task priority.
            name: Updated task name.
            description: Updated task description.
            parameters: Updated task parameters.
            properties: Updated task properties.
            schedule: Updated task schedule.
            overwriteParameters: Whether to overwrite parameters. Defaults to False.

        Returns:
            The updated task.

        Raises:
            MatchFailed: If the request parameters are invalid (400).
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            InternalServerError: If an internal server error occurs (500).
        """
        # prepare put request data
        data: dict[str, Any] = {}
        if labels:
            data['labels'] = labels
        if tags:
            data['tags'] = tags
        if debugLevel:
            data['debugLevel'] = debugLevel
        if priority:
            data['priority'] = priority
        if name:
            data['name'] = name
        if description:
            data['description'] = description
        if parameters:
            data['parameters'] = parameters
        if properties:
            data['properties'] = properties
        if schedule:
            data['schedule'] = schedule

        # send put request
        response: Response = self._api.put(
            endpoint=self._endpoint + f'task/{id}/',
            json=data,
            params={'overwriteParameters': overwriteParameters},
        )

        # validate response
        match response.status_code:
            case 200:  # OK
                return from_dict(
                    data_class=Task,
                    data=response.json(),
                    config=settings.dacite_config,
                )
            case 400:  # Match failed
                raise MatchFailed(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 401:  # Authentication failed
                raise AuthenticationError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 403:  # Permission denied
                raise PermissionError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case 500:  # Internal server error
                raise InternalServerError(
                    f'{response.status_code} - {response.json()["reason"]}'
                )
            case _:  # All other cases
                raise Exception(
                    f'Failed to update task. Response: {response.__dict__}'
                )

    def get_tasks(
        self, filters: dict | None = None
    ) -> tuple[list[Task], int, int, int, int]:
        """Get all tasks for this project.

        Args:
            filters: Optional dictionary of filters to apply to the task retrieval.

        Returns:
            A tuple containing:
                - List of tasks.
                - Limit (items per page).
                - Current page number.
                - Total pages.
                - Total count of items.

        Raises:
            AuthenticationError: If authentication fails (401).
            PermissionError: If permission is denied (403).
            ObjectNotFound: If the project is not found (404).
        """
        response: Response = self._api.get(
            endpoint=self._endpoint + 'tasks/',
            params=filters,
        )
        match response.status_code:
            case 200:  # OK
                data = response.json()
                tasks: list[Task] = [
                    from_dict(
                        data_class=Task,
                        data=task,
                        config=settings.dacite_config,
                    )
                    for task in data['items']
                ]
                limit: int = data['limit']
                page: int = data['page']
                totalPages: int = data['totalPages']
                totalCount: int = data['totalCount']
                return tasks, limit, page, totalPages, totalCount
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

    ############## Dunder Methods ##############
    def __post_init__(self):
        """Initialize the API endpoint after the object is created."""
        self._endpoint = f'project/{self._id}/'

    def __str__(self):
        """Return string representation of the object as its id."""
        return self._id
