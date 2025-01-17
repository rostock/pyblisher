from httpx import Response

class ExtResponse(Response):
    """
    An extended httpx.Response object with additional methods.
    """

    def ok(self):
        """
        Returns True if the response status code is 2xx.
        """
        if self.status_code >= 200 and self.status_code < 300:
            return True
        else:
            return False

    @classmethod
    def from_response(cls, response: Response):
        """
        Create an ExtResponse from a httpx.Response object.
        """
        return cls(
            status_code=response.status_code,
            headers=response.headers,
            content=response.content,
            request=response.request,
            extensions=response.extensions
        )
