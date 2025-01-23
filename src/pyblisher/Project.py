from dataclasses import dataclass, field
from typing import Optional

from src.pyblisher.client import ApiClient


@dataclass
class Project:
    """
    This class implements the structure of Projects of the VC Publisher API.

    :attribute _id: project id
    :atype _id: str
    :attribute name: project name
    :atype name: str
    :attribute description: project description
    :atype description: str
    :attribute bbox: project bounding box
    :atype bbox: list
    :attribute properties: project properties
    :atype properties: dict
    """

    _id: str
    name: str
    description: Optional[str] = ""
    bbox: Optional[list] = None
    properties: Optional[dict] = None
    _api: ApiClient = field(init=False, default=ApiClient(), repr=False)

    def __get_project__(self) -> bool:
        """
        Get a project by its id and updates object attributes.

        :return: ok
        :rtype: bool
        """
        pass

    def create_task(self, name: str, description: str) -> Task:
        return Task(name=name, description=description, api=self._api)
