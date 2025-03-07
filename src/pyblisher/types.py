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
    class. It defines the schedule of a Task.
    """

    type: Literal['immediate', 'scheduled', 'cron']


@dataclass
class ImmediateSchedule(Schedule):
    """
    ImmediateSchedule is a TypedDict that represents the schedule attribute of
    the Task class. It defines an immediate Task schedule.
    """

    type = 'immediate'


class ScheduledSchedule(Schedule):
    """
    ScheduledSchedule is a TypedDict that represents the schedule attribute of
    the Task class. It defines a scheduled Task schedule.
    """

    type = 'scheduled'
    scheduled: str  # datetime in isoformat
    suspended: Optional[bool]


class CronSchedule(Schedule):
    """
    CronSchedule is a TypedDict that represents the schedule attribute of the
    Task class. It defines a cron schedule for Tasks.
    """

    type = 'cron'
    scheduled: str  # datetime in isoformat
    cron: str
    suspended: Optional[bool]
