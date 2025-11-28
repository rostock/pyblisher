from dataclasses import dataclass
from typing import Any, Literal, Optional, Protocol

from httpx import Response


class ApiClientProtocol(Protocol):
    """Protocol defining the interface for API clients."""

    def get(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> Response:
        """Make a GET Request to the VC Publisher API.

        Args:
            endpoint: The API endpoint to request.
            params: Optional query parameters.

        Returns:
            Response object from the API.
        """
        ...

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        files: Optional[Any] = None,
    ) -> Response:
        """Make a POST Request to the VC Publisher API.

        Args:
            endpoint: The API endpoint to request.
            data: Optional form data.
            json: Optional JSON data.
            params: Optional query parameters.
            files: Optional files to upload.

        Returns:
            Response object from the API.
        """
        ...

    def delete(
        self,
        endpoint: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Response:
        """Make a DELETE Request to the VC Publisher API.

        Args:
            endpoint: The API endpoint to request.
            headers: Optional request headers.
            params: Optional query parameters.

        Returns:
            Response object from the API.
        """
        ...

    def put(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        files: Optional[Any] = None,
    ) -> Response:
        """Make a PUT Request to the VC Publisher API.

        Args:
            endpoint: The API endpoint to request.
            data: Optional form data.
            json: Optional JSON data.
            params: Optional query parameters.
            files: Optional files to upload.

        Returns:
            Response object from the API.
        """
        ...

    def stream(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> Any:
        """Make a streaming request to the VC Publisher API.

        Args:
            endpoint: The API endpoint to request.
            params: Optional query parameters.

        Returns:
            A streaming response generator.
        """
        ...


@dataclass
class SourceProperty:
    """Base class for source properties.

    SourceProperty is a dataclass that represents one structure of the
    sourceProperties attribute of the Source class.

    Attributes:
        type: The type of source ('external' or 'internal').
    """

    type: Literal['external', 'internal']


@dataclass
class ExternalSource(SourceProperty):
    """External source configuration.

    ExternalSource is a dataclass that represents an external source
    configuration for the sourceProperties attribute of the Source class.

    Attributes:
        type: The type of source, always 'external'.
        url: The URL of the external source.
    """

    type = 'external'
    url: str


@dataclass
class InternalSource(SourceProperty):
    """Internal source configuration.

    InternalSource is a dataclass that represents an internal source
    configuration for the sourceProperties attribute of the Source class.
    It defines the bucket and key of the internal source.

    Attributes:
        type: The type of source, always 'internal'.
        dataBucketId: The bucket id.
        dataBucketKey: The bucket key.
        urlSuffix: Optional URL suffix.
    """

    type = 'internal'
    dataBucketId: str
    dataBucketKey: str
    urlSuffix: Optional[str] = None


@dataclass
class Schedule:
    """Schedule configuration for tasks.

    Schedule is a dataclass that represents the schedule attribute of the Task
    class. There are three types of schedules: immediate, scheduled, and cron.

    For immediate schedules, only the type attribute is required.
    For scheduled schedules, the type and scheduled attributes are required.
    For cron schedules, the type and cron attributes are required.
    The suspended attribute is optional for scheduled and cron schedules.

    Attributes:
        type: The schedule type ('immediate', 'scheduled', or 'cron').
        scheduled: Optional datetime in isoformat for scheduled jobs.
        cron: Optional cron expression for cron jobs.
        suspended: Optional flag to suspend scheduled or cron jobs.
    """

    type: Literal['immediate', 'scheduled', 'cron']
    # for CronJobs and Scheduled Jobs, the scheduled attribute is required
    scheduled: Optional[str] = None  # datetime in isoformat
    # for CronJobs, the cron attribute is required
    cron: Optional[str] = None
    # for Scheduled Jobs and CronJobs, the suspended attribute is optional
    suspended: Optional[bool] = None

    def to_dict(self) -> dict:
        """Convert the Schedule to a dictionary.

        Returns:
            A dictionary representation of the schedule.
        """
        return self.__dict__
