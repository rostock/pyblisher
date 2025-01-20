from uuid import uuid4

from src.pyblisher.client import ApiClient


class DataBucket:
    """
    This class implements the structure of DataBuckets of the VC Publisher API.

    :attribute _id: data bucket id
    :atype _id: str
    :attribute name: data bucket name
    :atype name: str
    :attribute description: data bucket description
    :atype description: str
    :attribute properties: data bucket properties
    :atype properties: dict
    """

    __client: ApiClient = ApiClient()
    _project = __client.get_project_id()
    _id: str = ""
    name: str = ""
    description: str = ""
    properties: dict = {}

    def __init__(
        self,
        _id: str = None,
        name: str = str(uuid4()),
        description: str = "",
        properties=None,
    ):
        if properties is None:
            properties = {}
        if _id:
            # get data bucket information for given id
            self._id = _id
            self.__get_bucket__()
        else:
            # create new data bucket
            self.name = f"{name}_bucket"
            self.description = description
            self.properties = properties
            self.__create__()

    def __create__(self) -> None:
        """
        This method registers a new data bucket in the VCPublisher API and takes over its data.
        :return:
        """
        data: dict = {
            "name": self.name,
            "description": self.description,
            "properties": self.properties,
        }
        ok, bucket = self.__client.post(
            endpoint=f"/project/{self._project}/data-bucket/", data=data
        )
        if ok:
            self._id = bucket["_id"]
            self.name = bucket["name"]
            self.create_object(key=".keep")
            self.__client.logger.debug("Data Bucket created.")

    def __get_bucket__(self):
        """
        This method takes the data from an existing data bucket.
        :return:
        """
        ok, bucket = self.__client.get(
            endpoint=f"/project/{self._project}/data-bucket/{self._id}"
        )
        if ok:
            self.name = bucket["name"]
            self.description = bucket["description"]
            self.properties = bucket["properties"]
            self.projectId = bucket["projectId"]
        else:
            self.__client.logger.warning("Failed to get Bucket.")

    def create_object(self, key: str, object_type: str = "file"):
        """
        create an empty bucket object

        :param key: object key
        :param object_type: object type, default: `"file"`
        :return:
        """
        data = {"key": key, "type": object_type}
        self.__client.post(
            endpoint=f"/project/{self._project}/data_bucket/{self._id}", json=data
        )

    def delete(self):
        """
        delete Bucket

        :return: ok, response
        :rtype: tuple[bool, dict | Response | None]
        """
        endpoint = f"/project/{self._project}/data-bucket/{self._id}"
        ok, response = self.__client.delete(endpoint=endpoint)
        return ok, response

    def download_file(self, object_key: str, stream: bool = True):
        """
        download file from data bucket

        :param object_key: object key
        :ptype object_key: str
        :param stream: stream file, default: `True`
        :ptype stream: bool
        :return: ok, response
        :rtype: tuple[bool, dict | Response | None]
        """
        parameter = {"key": object_key}
        # print(headers)
        ok, response = self.__client.get(
            endpoint=f"/project/{self._project}/data-bucket/{self._id}/download-file",
            # headers=headers,
            stream=stream,
            params=parameter,
        )
        print(response.raw.__dict__)
        return ok, response

    def link(self) -> dict:
        """
        generate bucket information to link this object in tasks or sources

        :return:
        """
        data = {"type": "internal", "dataBucketId": self._id, "dataBucketKey": "/"}
        return data

    def upload(self, path: str = None, file: dict = None):
        """
        Uploads a file to the data bucket.

        :param path: path to uploaded file
        :ptype path: str
        :param file: or file
        :ptype file: dict
        :return: ok, key
        :rtype: tuple[bool, str]
        """
        key = list(file.keys())[0]
        if path:
            key = Path(path).name  # filename as key
            file = {key: open(path, "rb")}
        ok, response = self.__client.post(
            endpoint=f"/project/{self._project}/data-bucket/{self._id}/upload",
            files=file,
            # stream=True
            # celery job runs for every chunk with stream option
        )
        if not ok:
            print(response)
        # return data-bucket object key of uploadet file
        key = f"/{key}"
        return ok, key

    def delete_object(self, key):
        """
        delete object from data bucket

        :param key: object key
        :ptype key: str
        :return: ok, response
        :rtype: tuple[bool, dict | Response | None]
        """
        params = f"?key={key}"
        ok, response = self.__client.delete(
            endpoint=f"/project/{self._project}/data-bucket/{self._id}/object{params}",
        )
        return ok, response

    # GETTERS
    def get_endpoint(self):
        """
        get api endpoint of databucket object
        :return:
        """
        return f"/project/{self._project}/data-bucket/{self._id}"

    def get_id(self):
        """
        Returns the ID of the data bucket object.
        :return:
        """
        return self._id

    def get_key(self):
        """
        Returns the key of the data bucket object.
        :return:
        """
        return self.name

    def get_name(self):
        """
        Returns the name of the data bucket object.
        :return:
        """
        return self.name

    def get_url(self):
        """
        get API URL of this data bucket object
        :return:
        """
        return self.__client.get_url() + self.get_endpoint()
