from typing import Dict

from django.http import HttpRequest
from ninja import Router
from ralph.clients.registration.methods import register_user
from ralph.clients.registration.schemas import (
    RegistrationResponseSchema,
    RegistrationSchema,
)

router = Router()


@router.post("/register", response=RegistrationResponseSchema)
def user_login(request: HttpRequest, data: RegistrationSchema) -> Dict[str, str]:

    """
    Endpoint for registering a new user.

    Args:
        request (HttpRequest): HTTP Request.
        data (RegistrationSchema): Registration information on new user.

    Returns:
        RegistrationResponseSchema: Information on registered user.
    """

    return register_user(data)
