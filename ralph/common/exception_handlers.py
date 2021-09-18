from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI

from ninja.errors import ValidationError
from ralph.common.exceptions import (
    InvalidCredentialException,
    InvalidTokenException,
    UnauthorizedException,
    ValidationException,
)


def add_exception_handlers(api: NinjaAPI) -> None:

    """
    Add exception handlers to API.

    Args:
        api (NinjaAPI): API object.

    Returns:
        None.
    """

    # Add handler for UnauthorizedException.
    @api.exception_handler(UnauthorizedException)
    def on_not_authorized(
        request: HttpRequest, exc: UnauthorizedException
    ) -> HttpResponse:

        """
        Handler when user tries to access unauthorized content.
        """

        return api.create_response(
            request, {"message": f"Unauthorized. {str(exc)}."}, status=401
        )

    # Add handler for InvalidTokenException.
    @api.exception_handler(InvalidTokenException)
    def on_invalid_token(
        request: HttpRequest, exc: InvalidTokenException
    ) -> HttpResponse:

        """
        Handler when invalid token is passed to authorization.
        """

        return api.create_response(request, {"message": str(exc)}, status=400)

    # Add handler for InvalidCredentialException.
    @api.exception_handler(InvalidCredentialException)
    def on_invalid_credential(
        request: HttpRequest, exc: InvalidCredentialException
    ) -> HttpResponse:

        """
        Handler when credentials are incorrect.
        """

        return api.create_response(request, {"message": str(exc)}, status=400)

    # Add handler for ValidationException.
    @api.exception_handler(ValidationException)
    def on_validation_exception(
        request: HttpRequest, exc: ValidationException
    ) -> HttpResponse:

        """
        Handler when validation is not met.
        """

        return api.create_response(request, {"message": str(exc)}, status=400)

    # Add handler for ValidationError.
    @api.exception_handler(ValidationError)
    def on_validation_error(request: HttpRequest, exc: ValidationError) -> HttpResponse:

        """
        Handler when validation is not met.
        """

        # Get errors
        error = exc.errors[0]

        # Create error message
        error_msg = f"{error['loc'][-1]} - {error['msg']}"

        return api.create_response(request, {"message": error_msg}, status=400)
