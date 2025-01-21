from dataclasses import dataclass


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

    __id: str
    name: str
    description: str = ""
    bbox: list = None
    properties: dict = None

    def __create__(self) -> bool:
        """
        Create a new project

        :return: ok
        :rtype: bool
        """
        pass

    def __get_project__(self) -> bool:
        """
        Get a project by its id and updates object attributes.

        :return: ok
        :rtype: bool
        """
        pass

    def update(self) -> bool:
        """
        Update a project

        return: ok
        rtype: bool
        """
        pass

    def delete(self) -> bool:
        """
        Deletes this project.

        Admin role is needed.

        :return: ok
        :rtype: bool
        """
        pass

    def summary(self):
        """
        Returns statistics fot the project.

        Requires MEMBER or MANAGER permissions on this project.

        :return: project summary
        :rtype: dict
        """
        pass

    def get_database(self, database_id: str):
        """
        Get a database by its id

        :param database_id: database id
        :ptype database_id: str
        :return: database
        :rtype: Database
        """
        pass

    def __get_project__(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def summary(self):
        pass

    def get_database(self, database_id: str):
        """
        Get a database by its id
        :param database_id: database id
        :ptype database_id: str
        :return: database
        :rtype: Database
        """
        pass

    def get_databases(self):
        """
        retruns a list of all databases associated with this project

        :return: list of databases
        :rtype: list
        """
        pass

    def create_task(self, name: str, description: str):
        pass
