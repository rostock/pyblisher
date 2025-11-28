from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional

from .client import client
from .types import ApiClientProtocol, SourceProperty


@dataclass
class Source:
    """Implements the structure of Datasources of the VC Publisher API.

    Attributes:
        _id: Datasource id.
        name: Datasource name.
        properties: Datasource properties.
        typeProperties: Datasource type properties.
        sourceProperties: Source properties defining internal or external source.
        type: Datasource type (e.g. 'tileset', 'geojson', 'wms', etc.).
        dataUpdatedAt: Timestamp when data was last updated.
        dataUpdatedBy: User who last updated the data.
        projectId: Project id.
        uri: Datasource URI.
        jobIds: List of job ids.
        publishTaskIds: List of publish task ids.
        description: Optional datasource description.
        bbox: Optional bounding box.
    """

    # Internal attributes
    _api: ApiClientProtocol = field(default=client, init=False, repr=False)
    _endpoint: str = field(init=False, repr=False)

    # required api attributes
    _id: str
    name: str
    properties: dict
    typeProperties: dict
    sourceProperties: SourceProperty
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
    ]
    dataUpdatedAt: datetime
    dataUpdatedBy: str | None  # api could return it with value null
    projectId: str
    uri: str
    jobIds: list[str]
    publishTaskIds: list[str]

    # optional api attributes
    description: Optional[str] = ''
    bbox: Optional[list[float]] = None

    def publish(
        self,
        credentialsId: str,
        destination: str,
        numThreads: Optional[int],
        gzip: Optional[bool],
    ):
        """Publish the datasource with the given parameters.

        Not implemented yet.

        Args:
            credentialsId: Credentials id for publishing.
            destination: Destination for publishing.
            numThreads: Optional number of threads to use.
            gzip: Optional flag to enable gzip compression.
        """
        pass

    ############## Dunder Methods ##############
    def __post_init__(self):
        """Initialize the API endpoint after the object is created."""
        self._endpoint = f'project/{self.projectId}/datasource/{self._id}/'

    def __str__(self) -> str:
        return self._id
