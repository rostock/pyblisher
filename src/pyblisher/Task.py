from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .client import ApiClient, client
from .types import Schedule


@dataclass
class Task:
    """Implements the structure of Tasks of the VC Publisher API.

    Attributes:
        _api (ApiClient): The API client.
        _endpoint (str): The API endpoint.
        _id (str): Task id.
        createdAt (datetime): Task creation date.
        updatedAt (datetime): Task update date.
        createdBy (str): Task creator.
        updatedBy (str): Task last updater.
        labels (list): Task labels.
        properties (dict): Task properties.
        tags (dict): Task tags - additional metadata attributes not used by the Publisher.
        debugLevel (int): Task debug level.
        jobType (str): Task job type.
        jobVersion (str): Task job version.
        projectId (str): Project id.
        priority (int): Task priority.
        parameters (dict): Task parameters.
        schedule (dict): Task schedule.
        name (str): Task name.
        description (str): Task description.
        lastJobId (str): Task last job id.
    """

    # Internal attributes
    _api: ApiClient = field(default=client, init=False, repr=False)
    _endpoint: str = field(init=False, repr=False)

    # Required attributes
    _id: str
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str
    labels: list[str]
    properties: dict
    tags: dict
    debugLevel: int
    jobType: str
    jobVersion: str
    projectId: str
    priority: int
    parameters: dict
    schedule: Schedule

    # Optional attributes
    name: Optional[str]
    description: Optional[str]
    lastJobId: Optional[str]
    lastJob: Optional[dict]

    ############## Dunder Methods ##############
    def __post_init__(self):
        """Initialize the API endpoint after the object is created."""
        self._endpoint = f'project/{self.projectId}/task/{self._id}/'

    def __str__(self):
        """Return string representation of the Task object as its id."""
        return self._id
