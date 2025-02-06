from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .client import ApiClient


@dataclass
class Bucket:
    """
    This class implements the structure of Buckets of the VC Publisher API.

    :attribute _id: bucket id
    :atype _id: str
    :attribute name: bucket name
    :atype name: str
    :attribute description: bucket description
    :atype description: str
    :attribute properties: bucket properties
    :atype properties: dict
    :attribute projectId: project id
    :atype projectId: str
    """

    # Internal attributes
    _api: ApiClient = field(default=ApiClient(), init=False, repr=False)
    _endpoint: str = field(init=False, repr=False)

    # Required attributes
    _id: str
    createdAt: datetime
    updatedAt: datetime
    createdBy: str
    updatedBy: str
    name: str
    projectId: str

    # Optional attributes
    description: Optional[str] = None
    properties: Optional[dict] = None

    def upload(self, path: str):
        """
        Not imp lemented yet.
        Upload a file to this bucket.
        """
        pass

    def download(self, path: str):
        """
        Not implemented yet.
        Download a bucket object as `.tar.gz` from this bucket.
        """
        pass

    def download_file(self, key: str):
        """
        Not implemented yet.
        Download a bucket object from this bucket.
        """
        pass

    ############## Dunder Methods ##############
    def __post_init__(self):
        """
        Initialize the API endpoint, after the object is created.
        """
        self._endpoint = f'project/{self.projectId}/data-bucket/{self._id}/'
