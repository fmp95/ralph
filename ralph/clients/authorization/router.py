from ninja import Router

from ralph.clients.authorization.methods import login
from ralph.clients.authorization.schemas import LoginSchema, TokenOut

router = Router()


@router.post("/login", response=TokenOut)
def user_login(request: object, data: LoginSchema) -> TokenOut:

    """
    Endpoint for user login.

    This endpoint is used to generate a Bearer token.

    Args:
        data (LoginSchema): Credentials for login.

    Returns:
        TokenOut: Response with token information.
    """

    return {"token": login(**data.dict())}
