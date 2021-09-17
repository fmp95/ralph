class UnauthorizedException(Exception):

    """
    Custom exception for unauthorized access.

    This exception is raised when user tries to access content in which they don't
    have access.
    """

    ...


class InvalidTokenException(Exception):

    """
    Custom exception for invalid token.

    This exception is raised when an invalid token is passed with the request.
    """

    ...


class InvalidCredentialException(Exception):

    """
    Custom exception for invalid credential.

    This exception is raised when wrong credentials are passed in log in.
    """

    ...
