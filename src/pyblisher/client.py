from typing import Any, Optional

from httpx import Client, Response, post

from .auth import BearerAuth
from .Settings import settings
from .types import ApiClientProtocol


def log(event_name, info):
    """
    Logging function for httpx client trace extension.
    """
    print(event_name, info)


class ApiClient(ApiClientProtocol):
    _instance = None
    _connected = False
    _url: str = ''

    def __new__(cls):
        """
        Singleton Pattern
        """
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
        return cls._instance

    def __login__(self) -> bool:
        """
        Login to API
        :return: bearer token
        """
        if not self._connected:
            bearer: str = 'no bearer'
            self._url: str = f'{settings.host}/api/{settings.api_version}/'
            if self._url:
                response = post(
                    url=self._url + 'login/',
                    data={
                        'username': settings.user,
                        'password': settings.password,
                    },
                )
                if response.status_code == 200:
                    bearer: str = response.json()['token']
                    self._client = Client(base_url=f'{self._url}/')
                    self._client.auth = BearerAuth(bearer)
                    self._connected = True
                else:
                    raise Exception(f'Login failed: {response.__dict__}')
        return self._connected

    def __logout__(self) -> None:
        """
        logout from API
        """
        if self._connected:
            response = self._client.get(url=self._url + 'logout/')
            # should return 201 Logout Successful
            if response.status_code == 201:
                # self.logger.debug("Logout.")
                print('Logout.')
            else:
                # self.logger.warning(f"Logout failed: {response.json()}")
                print(f'Logout failed: {response.__dict__}')

    def get(self, endpoint: str, headers=None, *args, **kwargs) -> Response:
        """
        Make a GET Request to the VC Publisher API.

        :param endpoint: api endpoint like `projects/`
        :param headers:
        :param stream: just for file downloads, default False
        :return: Response
        """

        def get_it():
            """
            Get Request
            """
            url = self._url + endpoint
            response: Response = self._client.get(
                url=url, headers=headers, extensions={}
            )
            return response

        if self._connected:
            return get_it()
        else:
            if self.__login__():
                return get_it()
            else:
                response = Response(status_code=502)
                return response

    def post(
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json=None,
        files=None,
        *args,
        **kwargs,
    ) -> Response:
        """
        Make a POST Request to the VC Publisher API.

        :param endpoint: api endpoint like `project/`
        :param data: dictionary delivered in request body
        :param json:
        :param files:
        :return:
        """

        def post_it():
            """
            Post Request
            """
            url: str = self._url + endpoint
            response = self._client.post(
                url=url,
                data=data,
                json=json,
                files=files,
                extensions={},
            )
            return response

        if self._connected:
            return post_it()
        else:
            if self.__login__():
                return post_it()
            else:
                response = Response(status_code=502)
                return response

    def delete(self, endpoint: str, headers=None) -> Response:
        """
        Make a DELETE Request to the VC Publisher API.

        :param endpoint: api endpoint like `project/<project_id>/`
        :param headers: json like dict
        :return: Response as dict
        """

        def delete_it():
            """
            Delete Request
            """
            url: str = self._url + endpoint
            response = self._client.delete(
                url=url, headers=headers, extensions={'trace': log}
            )
            return response

        if self._connected:
            return delete_it()
        else:
            if self.__login__():
                return delete_it()
            else:
                response = Response(status_code=502)
                return response

    def put(
        self, endpoint: str, data: Optional[dict] = None, json=None, files=None
    ) -> Response:
        """
        Make a PUT Request to the VC Publisher API.
        """

        def put_it():
            """
            Put Request
            """
            url = self._url + endpoint
            response = self._client.put(
                url=url,
                data=data,
                json=json,
                files=files,
                extensions={'trace': log},
            )
            return response

        if self._connected:
            return put_it()
        else:
            if self.__login__():
                return put_it()
            else:
                response = Response(status_code=502)
                return response

    def stream(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> Any:
        """
        Führt einen Streaming-Request aus und gibt einen Generator zurück,
        der über die Bytes des Response iteriert. Der HTTP-Stream wird hier
        innerhalb eines with-Blocks geöffnet und automatisch geschlossen,
        wenn der Generator erschöpft ist.
        """

        def stream_it():
            """
            Stream Request
            """
            url = self._url + endpoint
            return self._client.stream(
                method='GET',
                url=url,
                params=params,
            )

        if self._connected:
            return stream_it()
        else:
            if self.__login__():
                return stream_it()
            else:
                response = Response(status_code=502)
                return response


client = ApiClient()
