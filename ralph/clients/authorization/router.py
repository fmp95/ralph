from typing import Dict

from django.http import HttpRequest
from ninja import Router

from ralph.clients.authorization.auth import Authorization, AuthorizationResponse
from ralph.clients.authorization.methods import login
from ralph.clients.authorization.schemas import LoginSchema, TokenOut

router = Router()


@router.post("/login", response=TokenOut)
def user_login(request: HttpRequest, data: LoginSchema) -> TokenOut:

    """
    Endpoint for user login.

    This endpoint is used to generate a Bearer token.

    Args:
        request (HttpRequest): HTTP request.
        data (LoginSchema): Credentials for login.

    Returns:
        TokenOut: Response with token information.
    """

    return {"token": login(**data.dict())}


@router.get("/user-profile", auth=Authorization())
def user_profile(request: HttpRequest) -> Dict[str, AuthorizationResponse]:

    """
    Endpoint for retrieving user profile.

    This endpoint is user to return all important user information to system.

    Args:
        request (HttpRequest): HTTP request.

    Returns:
        Dict[str, AuthorizationResponse]: Informations on user.
    """

    return {"data": request.auth}
