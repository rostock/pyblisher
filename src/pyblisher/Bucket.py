from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .client import client
from .types import ApiClientProtocol


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
    _api: ApiClientProtocol = field(default=client, init=False, repr=False)
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

    def upload(self, key: str, path: str):
        """
        Upload a file to this bucket.

        :param key: key of the file
        :type key: str
        :param path: path of the file
        :type path: str
        :return: Response
        :rtype: Response
        """
        with open(path, 'rb') as file:
            response = self._api.post(
                self._endpoint + 'upload/',
                files={key: file},
            )
        return response

    def download(self, key: str):
        """
        Downloads a bucket object or folder as `.tar.gz`.

        This method does not return the file content directly. Instead, it
        returns a generator, which yields the response content in chunks. You
        can iterate over the generator like over httpx streamed responses.
        Example:
            ```
            response = bucket.download()
            with open('download.tar.gz', 'wb') as file:
                for chunk in response.iter_bytes():
                    file.write(chunk)
            ```
        :return:
        """
        return self._api.stream(
            endpoint=self._endpoint + 'download/',
            params={'key': f'/{key}'},
        )

    def download_file(self, key: str):
        """
        Download a bucket object.

        This method does not return the file content directly. Instead, it
        returns a generator, which yields the response content in chunks. You
        can iterate over the generator like over httpx streamed responses.
        Example:
            ```
            response = bucket.download_file()
            with open('download', 'wb') as file:
                for chunk in response.iter_bytes():
                    file.write(chunk)
            ```
        """
        return self._api.stream(
            endpoint=self._endpoint + 'download-file/',
            params={'key': f'/{key}'},
        )

    ############## Dunder Methods ##############
    def __post_init__(self):
        """
        Initialize the API endpoint, after the object is created.
        """
        self._endpoint = f'project/{self.projectId}/data-bucket/{self._id}/'

    def __str__(self) -> str:
        return self._id
