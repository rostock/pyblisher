from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from httpx import Response

from .client import client
from .types import ApiClientProtocol


@dataclass
class Bucket:
    """Structure of Buckets of the VC Publisher API.

    Attributes:
        _id: Bucket id.
        name: Bucket name.
        description: Bucket description.
        properties: Bucket properties.
        projectId: Project id.
        createdAt: Bucket creation date.
        updatedAt: Bucket update date.
        createdBy: Bucket creator.
        updatedBy: Bucket last updater.
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

    def upload(self, key: str, path: str) -> Response:
        """Upload a file to this bucket.

        Args:
            key: Key of the file.
            path: Path of the file.

        Returns:
            Response object from the API.
        """
        with open(path, 'rb') as file:
            response = self._api.post(
                endpoint=self._endpoint + 'upload/',
                files={key: file},
            )
        return response

    def download(self, key: str):
        """Download a bucket object or folder as `.tar.gz`.

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

        Args:
            key: Key of the object or folder to download.

        Returns:
            A streaming response generator.
        """
        return self._api.stream(
            endpoint=self._endpoint + 'download/',
            params={'key': f'/{key}'},
        )

    def download_file(self, key: str):
        """Download a bucket object.

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

        Args:
            key: Key of the object to download.

        Returns:
            A streaming response generator.
        """
        return self._api.stream(
            endpoint=self._endpoint + 'download-file/',
            params={'key': f'/{key}'},
        )

    def delete_object(self, key: str):
        """Delete a bucket object.

        Args:
            key: Key of the object.

        Returns:
            Response object from the API.
        """
        return self._api.delete(
            endpoint=self._endpoint + 'object/',
            params={'key': f'/{key}'},
        )

    def delete(self):
        """Delete the bucket.

        Returns:
            Response object from the API.
        """
        return self._api.delete(endpoint=self._endpoint)

    def reference(self, dataBucketKey: str = '/'):
        """Return the Bucket as Reference Object for Datasource Creation or Task-Dataset-Parameters.

        Args:
            dataBucketKey: Key of the bucket. Defaults to "/".

        Returns:
            Bucket as Parameter Object for Dataset or Datasource definition.
        """
        return {
            'type': 'internal',
            'dataBucketId': self._id,
            'dataBucketKey': dataBucketKey,
        }

    ############## Dunder Methods ##############
    def __post_init__(self):
        """Initialize the API endpoint after the object is created."""
        self._endpoint = f'project/{self.projectId}/data-bucket/{self._id}/'

    def __str__(self) -> str:
        return self._id
