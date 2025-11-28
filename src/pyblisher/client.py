from typing import Any, Optional

from httpx import AsyncClient, Client, Response, post

from .auth import BearerAuth
from .Settings import settings
from .types import ApiClientProtocol


def log(event_name, info):
    """Log function for httpx client trace extension.

    Args:
        event_name: The name of the event being logged.
        info: Additional information about the event.
    """
    print(event_name, info)


class ApiClient(ApiClientProtocol):
    """API client for the VC Publisher API.

    This class implements the singleton pattern and provides methods for
    making HTTP requests to the VC Publisher API.

    Attributes:
        _instance: The singleton instance of the ApiClient.
        _connected: Whether the client is connected to the API.
        _url: The base URL of the API.
    """

    _instance = None
    _connected = False
    _url: str = ''

    def __new__(cls):
        """Create a singleton instance of the ApiClient.

        Returns:
            The singleton instance of the ApiClient.
        """
        if cls._instance is None:
            cls._instance = super(ApiClient, cls).__new__(cls)
        return cls._instance

    def __login__(self) -> bool:
        """Login to the API.

        Authenticates with the API using credentials from settings and
        initializes the HTTP clients with bearer token authentication.

        Returns:
            True if login was successful, False otherwise.

        Raises:
            Exception: If login fails with a non-200 status code.
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
                    bearer = response.json()['token']
                    self._client = Client(base_url=f'{self._url}/')
                    self._aclient = AsyncClient(base_url=f'{self._url}/')
                    self._client.auth = BearerAuth(bearer)
                    self._aclient.auth = BearerAuth(bearer)
                    self._connected = True
                else:
                    raise Exception(f'Login failed: {response.__dict__}')
        return self._connected

    def __logout__(self) -> None:
        """Logout from the API.

        Terminates the authenticated session with the API.
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

    def get(
        self, endpoint: str, params: Optional[dict] = None, *args, **kwargs
    ) -> Response:
        """Make a GET request to the VC Publisher API.

        Args:
            endpoint: API endpoint like `projects/`.
            params: Optional query parameters.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response object from the API.
        """

        def get_it():
            """Execute the GET request."""
            url = self._url + endpoint
            response: Response = self._client.get(
                url=url,
                params=params,
                extensions={},
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
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        files: Optional[Any] = None,
        *args,
        **kwargs,
    ) -> Response:
        """Make a POST request to the VC Publisher API.

        Args:
            endpoint: API endpoint like `project/`.
            data: Dictionary delivered in request body.
            json: JSON data to send.
            params: Query parameters.
            files: Files to upload.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response object from the API.
        """

        def post_it():
            """Execute the POST request."""
            url: str = self._url + endpoint
            response = self._client.post(
                url=url,
                data=data,
                json=json,
                params=params,
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

    def delete(
        self,
        endpoint: str,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> Response:
        """Make a DELETE request to the VC Publisher API.

        Args:
            endpoint: API endpoint like `project/<project_id>/`.
            headers: Optional dict for headers.
            params: Optional dict for query parameters.

        Returns:
            Response object from the API.
        """

        def delete_it():
            """Execute the DELETE request."""
            url: str = self._url + endpoint
            response = self._client.delete(
                url=url,
                headers=headers,
                params=params,
                extensions={'trace': log},
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
        self,
        endpoint: str,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        files: Optional[Any] = None,
    ) -> Response:
        """Make a PUT request to the VC Publisher API.

        Args:
            endpoint: The endpoint to PUT to.
            data: The data to PUT.
            json: The JSON data to PUT.
            params: The parameters to PUT.
            files: The files to PUT.

        Returns:
            Response object from the API.
        """

        def put_it():
            """Execute the PUT request."""
            url = self._url + endpoint
            response = self._client.put(
                url=url,
                data=data,
                json=json,
                params=params,
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

    async def stream(
        self,
        endpoint: str,
        params: Optional[dict] = None,
    ) -> Any:
        """Execute a streaming request and return a generator.

        Performs a streaming request that iterates over the bytes of the response.
        The HTTP stream is opened within a with-block and automatically closed
        when the generator is exhausted.

        Args:
            endpoint: API endpoint.
            params: Optional query parameters.

        Returns:
            A streaming response generator, or a Response with status 502 on failure.
        """

        async def stream_it():
            """Execute the stream request."""
            url = self._url + endpoint
            return self._aclient.stream(
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
