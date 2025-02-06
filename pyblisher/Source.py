from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .client import ApiClient


@dataclass
class Source:
    """
    This class implements the structure of Datasources of the VC Publisher API.

    :attribute _id: datasource id
    :atype _id: str
    :attribute name: datasource name
    :atype name: str
    :attribute description: datasource description
    :atype description: str
    :attribute typeProperties: datasource type properties
    :atype typeProperties: dict
    :attribute sourceProperties: datasource source properties
    :atype sourceProperties: dict
    :attribute type: datasource type
    :atype type: str
    """

    # Internal attributes
    _api: ApiClient = field(default=ApiClient(), init=False, repr=False)
    _endpoint: str = field(init=False, repr=False)
    # required api attributes
    _id: str
    name: str
    properties: dict
    typeProperties: dict
    sourceProperties: dict
    type: str
    dataUpdatedAt: datetime
    dataUpdatedBy: str | None
    projectId: str
    uri: str
    jobIds: list[str]
    publishTaskIds: list[str]
    # optional api attributes
    description: Optional[str] = ''
    bbox: Optional[list] = None

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
