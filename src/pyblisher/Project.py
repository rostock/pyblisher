from dataclasses import dataclass
from typing import Optional


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
    description: Optional[str] = ''
    bbox: Optional[list] = None
    properties: Optional[dict] = None

    def create_task(self, name: str, description: str):
        """
        Create a task for this project.
        """
        pass
