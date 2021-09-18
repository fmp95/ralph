from ralph.common.schemas import BaseModel


class LoginSchema(BaseModel):

    """
    Credentials insertion schema.

    Attributes:
        username (str): Username credential.
        password (str): Password credential.
    """

    username: str
    password: str


class TokenOut(BaseModel):

    """
    Response for valid credentials.

    Attributes:
        token (str): Token generated to user.
    """

    token: str
