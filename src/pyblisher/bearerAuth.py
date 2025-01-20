from httpx import Auth, Request


class BearerAuth(Auth):
    """
    Extends the httpx library with the option to authenticate with a bearer token at a Rest API.
    """

    token: str  # Bearer token
    scheme: str = "Bearer"

    def __init__(self, token: str):
        self.token: str = token

    def auth_flow(self, request: Request):
        # Add the bearer token to the request header
        request.headers["authorization"] = f"{self.scheme} {self.token}"
        yield request
