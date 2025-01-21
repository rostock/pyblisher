from httpx import Client, request

from src.pyblisher.bearerAuth import BearerAuth
from src.pyblisher.response import ExtResponse
from src.pyblisher.settings import settings


class ApiClient:
    def __init__(self):
        self.__url: str
        self._api_version: str = settings.VCP_API_VERSION
        self.__project_id = settings.VCP_PROJECT_ID
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
                response = ExtResponse.from_response(
                    response=request(
                        method="POST",
                        url=f"{self.__url}/login/",
                        auth=(settings.USER, settings.PASSWORD),
                        headers={"Content-Type": "application/json"},
                    )
                )
                if response.ok:
                    bearer: str = response.json()["token"]
                    self._client = Client(base_url=self.__url)
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
            if response.ok:
                self.logger.debug("Logout.")
            else:
                self.logger.warning(f"Logout failed: {response.json()}")

    def get(
        self, endpoint: str, headers=None, stream: bool = False, *args, **kwargs
    ) -> tuple[bool, dict | Response | None]:
        """
        Make a GET Request to the VC Publisher API.

        :param endpoint: api endpoint like `/projects/`
        :param headers:
        :param stream: just for file downloads, default False
        :return: Response as dict
        """

        def get_it():
            url: str = self.__url + endpoint
            response = self._client.get(
                url=url, headers=headers, stream=stream, *args, **kwargs
            )

            if response.ok and response.status_code != 204:
                self.logger.debug(f"GET {url}")
                if stream:
                    return response.ok, response
                else:
                    return response.ok, response.json()
            elif response.status_code == 204:
                # 204 No Response
                self.logger.debug(f"GET {url}")
                return response.ok, None
            else:
                self.logger.warning(f"GET on {url} failed: {response.json()}")
                return response.ok, response

        if self._connected:
            get_it()
        else:
            if self.__login__():
                get_it()
            else:
                response = Response()
                response.status_code = 502
                response.reason = "Bad Gateway. VCPub Object is not connected."
                return False, response

    def post(
        self,
        endpoint: str,
        data: dict = None,
        json=None,
        files=None,
        *args,
        **kwargs,
    ) -> tuple[bool, dict | Response | None]:
        """
        Make a POST Request to the VC Publisher API.

        :param endpoint: api endpoint like `/project/`
        :param data: dictionary delivered in request body
        :param json:
        :param files:
        :return:
        """

        def post_it():
            url: str = self.__url + endpoint
            response = self._client.post(
                url=url, data=data, json=json, files=files, *args, **kwargs
            )
            if response.ok and response.status_code != 204:
                self.logger.debug(f"POST {url}")
                return response.ok, response.json()
            elif response.status_code == 204:
                # 204 No Response
                self.logger.debug(f"POST {url}")
                return response.ok, None
            else:
                self.logger.warning(
                    f"POST on {url} failed: {response.__dict__}"
                )
                return response.ok, response

        if self._connected:
            post_it()
        else:
            if self.__login__():
                post_it()
            else:
                response = Response()
                response.status_code = 502
                response.reason = "Bad Gateway. VCPub Object is not connected."
                return False, response

    def delete(
        self, endpoint: str, headers=None
    ) -> tuple[bool, dict | Response | None]:
        """
        Make a DELETE Request to the VC Publisher API.

        :param endpoint: api endpoint like `/project/<project_id>/`
        :param headers: json like dict
        :return: Response as dict
        """

        def delete_it():
            url: str = self.__url + endpoint
            response = self._client.delete(url=url, headers=headers)
            if response.ok and response.status_code != 204:
                self.logger.debug(f"DELETE {url}")
                return response.ok, response.json()
            elif response.status_code == 204:
                # 204 No Response
                self.logger.debug(f"DELETE {url}")
                return response.ok, None
            else:
                self.logger.warning(
                    f"DELETE on {url} failed: {response.json()}"
                )
                return response.ok, response

        if self._connected:
            delete_it()
        else:
            if self.__login__():
                delete_it()
            else:
                response = Response()
                response.status_code = 502
                response.reason = "Bad Gateway. VCPub Object is not connected."
                return False, response

    def get_projects(self):
        """
        Get all projects
        :return: list of projects
        """
        pass

    def get_databases(self):
        """
        Get all databases
        :return: list of databases
        """
        pass
