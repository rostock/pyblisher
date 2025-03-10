from dataclasses import dataclass
from typing import Any, Literal, Optional, Protocol

from httpx import Response


class ApiClientProtocol(Protocol):
    def get(self, endpoint: str) -> Response:
        """
        Make a GET Request to the VC Publisher API.

        :return: Response as dict
        """
        ...

    def post(
        self, endpoint: str, data: Optional[dict] = None, json=None, files=None
    ) -> Response:
        """
        Make a POST Request to the VC Publisher API.

        :return: Response as dict
        """
        ...

    def delete(self, endpoint: str) -> Response:
        """
        Make a DELETE Request to the VC Publisher API.

        :return: Response as dict
        """
        ...

    def put(
        self, endpoint: str, data: Optional[dict] = None, json=None, files=None
    ) -> Response:
        """
        Make a PUT Request to the VC Publisher API.
        """
        ...

    def stream(self, endpoint: str, params: Optional[dict] = None) -> Any:
        """
        Make a streaming request to the VC Publisher API.

        :param endpoint: API endpoint
        :type endpoint: str
        :param params: query parameters
        :type params: Optional[dict]
        """
        ...


@dataclass
class SourceProperty:
    """
    SourceProperty is a dataclass that represents one structure of the
    sourceProperties attribute of the Source class.
    """

    type: Literal['external', 'internal']


@dataclass
class ExternalSource(SourceProperty):
    """
    ExternalSource is a dataclass that represents one structure of the
    sourceProperties attribute of the Source class.
    """

    type = 'external'
    url: str


@dataclass
class InternalSource(SourceProperty):
    """
    InternalSource is a dataclass that represents one structure of the
    sourceProperties attribute of the Source class.
    It defines the bucket and key of the internal source.
    """

    type = 'internal'
    dataBucketId: str
    dataBucketKey: str
    urlSuffix: Optional[str]


@dataclass
class Schedule:
    """
    Schedule is a TypedDict that represents the schedule attribute of the Task
    class.
    There are three types of schedules: immediate, scheduled, and cron.
    For immediate schedules, the type attribute is required.
    For scheduled schedules, the type and scheduled attributes are required.
    For cron schedules, the type and cron attributes are required.
    The suspended attribute is optional for scheduled and cron schedules.

    :attr type: Literal['immediate', 'scheduled', 'cron']
    :attr scheduled: Optional[str]
    :attr cron: Optional[str]
    :attr suspended: Optional[bool]
    """

    type: Literal['immediate', 'scheduled', 'cron']
    # for CronJobs and Scheduled Jobs, the scheduled attribute is required
    scheduled: Optional[str] = None  # datetime in isoformat
    # for CronJobs, the cron attribute is required
    cron: Optional[str] = None
    # for Scheduled Jobs and CronJobs, the suspended attribute is optional
    suspended: Optional[bool] = None
