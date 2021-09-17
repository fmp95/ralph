from ninja import Schema


class LoginSchema(Schema):

    """
    Credentials insertion schema.

    Attributes:
        username (str): Username credential.
        password (str): Password credential.
    """

    username: str
    password: str


class TokenOut(Schema):

    """
    Response for valid credentials.

    Attributes:
        token (str): Token generated to user.
    """

    token: str
