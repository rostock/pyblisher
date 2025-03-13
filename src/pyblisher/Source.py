from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional

from .client import client
from .types import ApiClientProtocol, SourceProperty


@dataclass
class Source:
    """
    This class implements the structure of Datasources of the VC Publisher API.
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
        """
        Not implemented yet.
        Publish the datasource with the given parameters.
        """
        pass

    ############## Dunder Methods ##############
    def __post_init__(self):
        """
        This function is called after the initialization of the object.
        """
        self._endpoint = f'project/{self.projectId}/datasource/{self._id}/'

    def __str__(self) -> str:
        return self._id
