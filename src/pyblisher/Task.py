from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.pyblisher.client import ApiClient
from src.pyblisher.databucket import DataBucket
from src.pyblisher.datasource import Datasource


@dataclass
class Task:
    """
    This class implements the structure of Tasks of the VC Publisher API.

    :attribute _id: task id
    :atype _id: str
    :attribute name: task name
    :atype name: str
    :attribute description: task description
    :atype description: str
    :attribute jobType: task job type
    :atype jobType: str
    :attribute parameters: task parameters
    :atype parameters: dict
    :attribute schedule: task schedule
    :atype schedule: dict
    """

    _client: ApiClient = field(repr=False)
    _id: str = ""
    name: str = ""
    description: str = ""
    jobType: str = "pointcloud"
    parameters: dict = {
        "epsgCode": 25833,
        "command": "conversion",
        "dataset": {},
        "datasource": {},
    }
    schedule: dict = {"type": "immediate"}

    def __init__(
        self, _id: str = None, name: str = str(uuid4()), description: str = ""
    ):
        if _id:
            self._id = _id
            self.__get_task__()
        else:
            self.name = f"dw_{name.lower().replace(' ', '_')}"
            self.description = description
            self.__create__()

    def __create__(self):
        bucket = DataBucket(name=self.name, description=self.description)
        source = Datasource(name=self.name, description=self.description)
        self.parameters["dataset"] = bucket.link()
        self.parameters["datasource"] = source.link()
        current_time = datetime.now(timezone.utc)
        scheduled_time = current_time + timedelta(minutes=30)
        self.schedule = {
            "type": "scheduled",
            "scheduled": f"{scheduled_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')}",
        }
        data = {
            "name": self.name,
            "description": self.description,
            "jobType": self.jobType,
            "parameters": self.parameters,
            "schedule": self.schedule,
        }
        ok, task = self.__client.post(
            endpoint=f"/project/{self._project}/task/", json=data
        )
        self._id = task["_id"]
        if ok:
            self.__client.logger.debug("Task created.")

    def __get_task__(self):
        ok, task = self.__client.get(
            endpoint=f"/project/{self._project}/task/{self._id}/"
        )
        if ok:
            self.name = task["name"]
            self.jobType = task["jobType"]
            self.parameters = task["parameters"]
            self.schedule = task["schedule"]
        else:
            self.__client.logger.warning("Failed to get Task.")

    def get_dataset(self):
        """
        get dataset of a task.
        :return:
        """
        return self.parameters["dataset"]

    def get_datasource(self):
        """
        get dataset of a task.
        :return:
        """
        return self.parameters["datasource"]

    def get_endpoint(self):
        """
        get api endpoint of task object
        :return:
        """
        return f"/project/{self._project}/task{self._id}"

    def get_id(self):
        """
        get task id
        :return:
        """
        return self._id
