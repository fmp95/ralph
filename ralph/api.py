from ninja import NinjaAPI

from ralph.clients.authorization.router import router as authentication_router
from ralph.clients.check.router import router as check_router
from ralph.common.exceptions import (
    InvalidCredentialException,
    InvalidTokenException,
    UnauthorizedException,
)

api = NinjaAPI()

# Add routes.
api.add_router("", authentication_router)
api.add_router("", check_router)

# Add handler for UnauthorizedException.
@api.exception_handler(UnauthorizedException)
def on_not_authorized(
    request: object,
    exc: UnauthorizedException,  # pylint: disable = unused-argument
) -> object:

    """
    Handler when user tries to access unauthorized content.
    """

    return api.create_response(request, {"message": "Unauthorized."}, status=401)


# Add handler for InvalidTokenException.
@api.exception_handler(InvalidTokenException)
def on_invalid_token(
    request: object,
    exc: InvalidTokenException,  # pylint: disable = unused-argument
) -> object:

    """
    Handler when invalid token is passed to authorization.
    """

    return api.create_response(request, {"message": "Invalid token."}, status=400)


# Add handler for InvalidCredentialException.
@api.exception_handler(InvalidCredentialException)
def on_invalid_credential(
    request: object,
    exc: InvalidCredentialException,  # pylint: disable = unused-argument
) -> object:

    """
    Handler when credentials are incorrect.
    """

    return api.create_response(
        request, {"message": "Username and/or password are incorrect."}, status=400
    )
