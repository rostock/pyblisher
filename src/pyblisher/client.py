from httpx import Client, request

from src.pyblisher.bearerAuth import BearerAuth
from src.pyblisher.response import ExtResponse
from src.pyblisher.settings import settings


class ApiClient:
    def __init__(self):
        self.__project_id = settings.VCP_API_PROJECT_ID
        self.__data_path = (
            "/vcs/data/public/"  # im root System unter /nfs/daten/rostock3d/vcpublisher
        )
        self.__epsg = "25833"
        self.__connected = False

    def __login__(self) -> bool:
        """
        Login to API
        :return: bearer token
        """
        if not self.__connected:
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
                    self.__session = Client(base_url=self.__url)
                    self.__session.auth = BearerAuth(bearer)
                    self.__connected = True
                else:
                    raise Exception(f"Login failed: {response.__dict__}")
        return self.__connected

    def __logout__(self) -> None:
        """
        logout from API
        """
        if self.__connected:
            response = self.__session.get(url=f"{self.__url}/logout/")
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
            response = self.__session.get(
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

        if self.__connected:
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
        self, endpoint: str, data: dict = None, json=None, files=None, *args, **kwargs
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
            response = self.__session.post(
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
                self.logger.warning(f"POST on {url} failed: {response.__dict__}")
                return response.ok, response

        if self.__connected:
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
            response = self.__session.delete(url=url, headers=headers)
            if response.ok and response.status_code != 204:
                self.logger.debug(f"DELETE {url}")
                return response.ok, response.json()
            elif response.status_code == 204:
                # 204 No Response
                self.logger.debug(f"DELETE {url}")
                return response.ok, None
            else:
                self.logger.warning(f"DELETE on {url} failed: {response.json()}")
                return response.ok, response

        if self.__connected:
            delete_it()
        else:
            if self.__login__():
                delete_it()
            else:
                response = Response()
                response.status_code = 502
                response.reason = "Bad Gateway. VCPub Object is not connected."
                return False, response
