class ObjectNotFound(Exception):
    """
    404 - Object not found Exception.
    """

    def __init__(self, message):
        super().__init__(message)


class AuthenticationError(Exception):
    """
    401 - Authentication Error.
    """

    def __init__(self, message):
        super().__init__(message)


class PermissionError(Exception):
    """
    403 - Permission Error.
    """

    def __init__(self, message):
        super().__init__(message)
