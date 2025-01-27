from httpx import Auth


class UserPassAuth(Auth):
    """
    Extends the httpx library with the option to authenticate with a
    user-password tuple at a Rest API.
    """

    user: str  # User
    password: str  # Password

    def __init__(self, user: str, password: str):
        self.user: str = user
        self.password: str = password

    def auth_flow(self, request):
        # Add the user and password to the request header
        request.headers['username'] = self.user
        request.headers['password'] = self.password
        yield request
