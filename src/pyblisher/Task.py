from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .client import ApiClient, client
from .types import Schedule


@dataclass
class Task:
    """
    This class implements the structure of Tasks of the VC Publisher API.

    # Internal attributes
    This are attributes, which are not overgiven by the API, but are necessary
    for the object to work. They might not be initialized.

    :attribute _api: The API client
    :atype _api: ApiClient
    :attribute _endpoint: The API endpoint
    :atype _endpoint: str

    # Required attributes
    This are attributes, which are definitly overgiven by the API.

    :attribute _id: task id
    :atype _id: str
    :attribute createdAt: task creation date
    :atype createdAt: datetime
    :attribute updatedAt: task update date
    :atype updatedAt: datetime
    :attribute createdBy: task creator
    :atype createdBy: str
    :attribute updatedBy: task last updater
    :atype updatedBy: str
    :attribute labels: task labels
    :atype labels: list
    :attribute properties: task properties
    :atype properties: dict
    :attribute tags: task tags
    :atype tags: dict
    :attribute debugLevel: task debug level
    :atype debugLevel: int
    :attribute jobType: task job type
    :atype jobType: str
    :attribute jobVersion: task job version
    :atype jobVersion: str
    :attribute projectId: project id
    :atype projectId: str
    :attribute priority: task priority
    :atype priority: int
    :attribute parameters: task parameters
    :atype parameters: dict
    :attribute schedule: task schedule
    :atype schedule: dict

    # Optional attributes, which are not necessarily overgiven by the API
    :attribute name: task name
    :atype name: str
    :attribute description: task description
    :atype description: str
    :attribute lastJobId: task last job id
    :atype lastJobId: str
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

    ############## Dunder Methods ##############
    def __post_init__(self):
        """
        Initialize the API endpoint, after the object is created.
        """
        self._endpoint = f'project/{self.projectId}/task/{self._id}/'

    def __str__(self):
        """
        String representation of the Task object as its id.
        """
        return self._id
