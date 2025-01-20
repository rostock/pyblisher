from uuid import uuid4

from src.pyblisher.client import ApiClient
from src.pyblisher.databucket import DataBucket


class Datasource:
    """
    This class implements the structure of Datasources of the VC Publisher API.

    :attribute _id: datasource id
    :atype _id: str
    :attribute name: datasource name
    :atype name: str
    :attribute description: datasource description
    :atype description: str
    :attribute typeProperties: datasource type properties
    :atype typeProperties: dict
    :attribute sourceProperties: datasource source properties
    :atype sourceProperties: dict
    :attribute type: datasource type
    :atype type: str
    """

    __client: ApiClient = ApiClient()
    _project = __client.get_project_id()
    _id: str = ""
    name: str = ""
    description: str = ""
    typeProperties: dict = {}
    sourceProperties: dict = {}
    type: str = "tileset"

    def __init__(
        self, _id: str = None, name: str = str(uuid4()), description: str = ""
    ):
        if _id:
            self._id = _id
            self.__get_source__()
        else:
            self.name = f"{name}_source"
            self.description = description
            source_bucket = DataBucket(name=self.name, description=self.description)
            self.sourceProperties = source_bucket.link()
            self.__create__()

    def __create__(self):
        """
        create datasource at VCPub API
        :return:
        """
        data = {
            "name": self.name,
            "description": self.description,
            "typeProperties": self.typeProperties,
            "sourceProperties": self.sourceProperties,
            "type": self.type,
        }
        ok, source = self.__client.post(
            endpoint=f"/project/{self._project}/datasource", json=data
        )
        if ok:
            self.__client.logger.debug("Data Source created.")
            self._id = source["_id"]

    def __get_source__(self):
        """
        get datasource informations from VCPub API of an existing datasource
        :return:
        """
        ok, source = self.__client.get(
            endpoint=f"/project/{self._project}/datasource/{self._id}"
        )
        if ok:
            self.name = source["name"]
            self.description = source["description"]
            self.typeProperties = source["typeProperties"]
            self.sourceProperties = source["sourceProperties"]
            self.type = type
        else:
            self.__client.logger.warning("Failed to get Data Source.")

    def link(self):
        """
        create datasource link object as dict

        :return: datasource link data
        :rtype: dict
        """
        data = {"command": "update", "datasourceId": self._id}
        return data

    def delete(self):
        """
        delete Datasource
        :return:
        """
        pass
        # delete datasource bucket
        bucket = DataBucket(_id=self.sourceProperties["dataBucketId"])
        bucket.delete()
        # delete source
        self.__client.delete(endpoint=f"/project/{self._project}/datasource")
        # delete source object
        global_ref = globals()
        for var_name, var_obj in list(global_ref.items()):
            if var_obj is self:
                del global_ref[var_name]

    def get_endpoint(self):
        """
        get api endpoint of datasource object
        :return:
        """
        return f"/project/{self._project}/datasource/{self._id}"

    def get_url(self):
        """
        get API URL of this datasource
        :return:
        """
        return self.__client.get_url() + self.get_endpoint()
