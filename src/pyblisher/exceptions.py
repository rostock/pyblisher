class MatchFailed(Exception):
    """400 - Match Failed Error.

    Raised when the request parameters fail validation or matching.
    """

    def __init__(self, message):
        """Initialize MatchFailed exception.

        Args:
            message: The error message.
        """
        super().__init__(message)


class AuthenticationError(Exception):
    """401 - Authentication Error.

    Raised when authentication fails due to invalid credentials.
    """

    def __init__(self, message):
        """Initialize AuthenticationError exception.

        Args:
            message: The error message.
        """
        super().__init__(message)


class PermissionError(Exception):
    """403 - Permission Error.

    Raised when the user does not have permission to perform the action.
    """

    def __init__(self, message):
        """Initialize PermissionError exception.

        Args:
            message: The error message.
        """
        super().__init__(message)


class ObjectNotFound(Exception):
    """404 - Object not found Exception.

    Raised when the requested object does not exist.
    """

    def __init__(self, message):
        """Initialize ObjectNotFound exception.

        Args:
            message: The error message.
        """
        super().__init__(message)


class InternalServerError(Exception):
    """500 - Internal Server Error.

    Raised when the server encounters an internal error.
    """

    def __init__(self, message):
        """Initialize InternalServerError exception.

        Args:
            message: The error message.
        """
        super().__init__(message)
