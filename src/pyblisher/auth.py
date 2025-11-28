from httpx import Auth, Request


class BearerAuth(Auth):
    """Extend httpx library with bearer token authentication.

    This class extends the httpx library with the option to authenticate
    with a bearer token at a REST API.

    Attributes:
        token: The bearer token for authentication.
        scheme: The authentication scheme. Defaults to 'Bearer'.
    """

    token: str  # Bearer token
    scheme: str = 'Bearer'

    def __init__(self, token: str):
        """Initialize BearerAuth with a token.

        Args:
            token: The bearer token for authentication.
        """
        self.token: str = token

    def auth_flow(self, request: Request):
        """Add the bearer token to the request header.

        Args:
            request: The HTTP request to authenticate.

        Yields:
            The authenticated request.
        """
        request.headers['authorization'] = f'{self.scheme} {self.token}'
        yield request


class UserPassAuth(Auth):
    """Extend httpx library with user-password authentication.

    This class extends the httpx library with the option to authenticate
    with a user-password tuple at a REST API.

    Attributes:
        user: The username for authentication.
        password: The password for authentication.
    """

    user: str  # User
    password: str  # Password

    def __init__(self, user: str, password: str):
        """Initialize UserPassAuth with user and password.

        Args:
            user: The username for authentication.
            password: The password for authentication.
        """
        self.user: str = user
        self.password: str = password

    def auth_flow(self, request):
        """Add the user and password to the request header.

        Args:
            request: The HTTP request to authenticate.

        Yields:
            The authenticated request.
        """
        request.headers['username'] = self.user
        request.headers['password'] = self.password
        yield request
