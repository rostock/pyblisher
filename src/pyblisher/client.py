from httpx import Client, Response, codes, request

from src.pyblisher.bearerAuth import BearerAuth
from src.pyblisher.settings import settings


def log(event_name, info):
    """
    Logging function for httpx client trace extension.
    """
    print(event_name, info)


class ApiClient:
    def __init__(
        self,
        url: str = settings.HOST,
        api_version: str = settings.API_VERSION,
        project_id: str = settings.PROJECT_ID,
    ):
        self.__url: str = url
        self._api_version: str = api_version
        self.__project_id: str = project_id
        self._connected = False

    def __login__(self) -> bool:
        """
        Login to API
        :return: bearer token
        """
        if not self._connected:
            bearer: str = "no bearer"
            self.__url: str = settings.HOST
            if self.__url:
                response = request(
                    method="POST",
                    url=f"{self.__url}/login/",
                    auth=(settings.USER, settings.PASSWORD),
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code == codes.OK:
                    bearer: str = response.json()["token"]
                    self._client = Client(
                        base_url=f"{self.__url}/api/{self._api_version}/"
                    )
                    self._client.auth = BearerAuth(bearer)
                    self._connected = True
                else:
                    raise Exception(f"Login failed: {response.__dict__}")
        return self._connected

    def __logout__(self) -> None:
        """
        logout from API
        """
        if self._connected:
            response = self._client.get(url=f"{self.__url}/logout/")
            # should return 201 Logout Successful
            if response.status_code == 201:
                # self.logger.debug("Logout.")
                print("Logout.")
            else:
                # self.logger.warning(f"Logout failed: {response.json()}")
                print(f"Logout failed: {response.__dict__}")

    def get(
        self, endpoint: str, headers=None, stream: bool = False, *args, **kwargs
    ) -> Response:
        """
        Make a GET Request to the VC Publisher API.

        :param endpoint: api endpoint like `/projects/`
        :param headers:
        :param stream: just for file downloads, default False
        :return: Response
        """

        def get_it():
            """
            Get Request
            """
            url: str = self.__url + endpoint
            response = self._client.get(
                url=url, headers=headers, extensions={"trace": log}
            )
            return response

        if self._connected:
            get_it()
        else:
            if self.__login__():
                get_it()
            else:
                response = Response(status_code=502)
                return response

    def post(
        self,
        endpoint: str,
        data: dict = None,
        json=None,
        files=None,
        *args,
        **kwargs,
    ) -> Response:
        """
        Make a POST Request to the VC Publisher API.

        :param endpoint: api endpoint like `/project/`
        :param data: dictionary delivered in request body
        :param json:
        :param files:
        :return:
        """

        def post_it():
            """
            Post Request
            """
            url: str = self.__url + endpoint
            response = self._client.post(
                url=url,
                data=data,
                json=json,
                files=files,
                extensions={"trace": log},
            )
            return response

        if self._connected:
            post_it()
        else:
            if self.__login__():
                post_it()
            else:
                response = Response(status_code=502)
                return response

    def delete(self, endpoint: str, headers=None) -> Response:
        """
        Make a DELETE Request to the VC Publisher API.

        :param endpoint: api endpoint like `/project/<project_id>/`
        :param headers: json like dict
        :return: Response as dict
        """

        def delete_it():
            """
            Delete Request
            """
            url: str = self.__url + endpoint
            response = self._client.delete(
                url=url, headers=headers, extensions={"trace": log}
            )
            return response

        if self._connected:
            delete_it()
        else:
            if self.__login__():
                delete_it()
            else:
                response = Response(status_code=502)
                return response

    def put(
        self, endpoint: str, data: dict = None, json=None, files=None
    ) -> Response:
        """
        Make a PUT Request to the VC Publisher API.
        """

        def put_it():
            """
            Put Request
            """
            url = self.__url + endpoint
            response = self._client.put(
                url=url,
                data=data,
                json=json,
                files=files,
                extensions={"trace": log},
            )
            return response

        if self._connected:
            put_it()
        else:
            if self.__login__():
                put_it()
            else:
                response = Response(status_code=502)
                return response

    def stream(
        self,
        method: str,
        endpoint: str,
        data: dict = None,
        json=None,
        files=None,
    ):
        """
        Stream a request
        """
        url = self.__url + endpoint
        response = self._client.stream(
            method=method,
            url=url,
            data=data,
            json=json,
            files=files,
            extensions={"trace": log},
        )
        return response

    def get_projects(self):
        """
        not implemented yet

        Get all projects

        :return: list of projects
        """
        pass

    def get_databases(self):
        """
        not implemented yet

        Get all databases

        :return: list of databases
        """
        pass
