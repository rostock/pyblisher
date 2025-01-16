from httpx import Auth, Request

class BearerAuth(Auth):
    """
    Extends the httpx library with the option to authenticate with a bearer token at a Rest API.
    """
    def __init__(self, token: str):
        self.token: str = token
        self.scheme = "Bearer"

    def auth_flow(self, request: Request) -> Request:
        request.headers["authorization"] = f"{self.scheme} {self.token}"
        return request
