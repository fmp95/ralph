from pydantic import validator

from ralph.clients.registration.validations import (
    check_same_password,
    validates_password_format,
    validates_username_format,
)
from ralph.common.schemas import BaseModel


class RegistrationSchema(BaseModel):

    """
    Schema used to validate registration object.

    Attributes:
        username (constr): User's username.
        password (str): User's password.
        password_confirm (str): User's password confirmation.
        email (str): User's e-mail addres.
        first_name (str): User's first_name.
        last_name (str): User's last_name.
        terms_accepted (bool): Acceptance of terms of condition.
        _password_format (str): Validation of password format.
        _confirm_password (str): Validation of passwords matching.
    """

    username: str
    password: str
    password_confirm: str
    email: str
    first_name: str
    last_name: str
    terms_accepted: bool

    # Validates username format.
    _username_format = validator("username", allow_reuse=True)(
        validates_username_format
    )

    # Validates password format.
    _password_format = validator("password", allow_reuse=True)(
        validates_password_format
    )

    # Check if password and password_confirm match.
    _confirm_password = validator("password_confirm", allow_reuse=True)(
        check_same_password
    )


class RegistrationConfirmationSchema(BaseModel):

    """
    Schema used with registered user information.

    Attributes:
        uuid (str): User's unique identifier.
        username (constr): User's username.
        email (str): User's e-mail addres.
        first_name (str): User's first_name.
        last_name (str): User's last_name.
    """

    uuid: str
    username: str
    email: str
    first_name: str
    last_name: str


class RegistrationResponseSchema(BaseModel):

    """
    Schema to respond to user's request.

    Attributes:
        data (RegistrationConfirmationSchema): User's information.
    """

    data: RegistrationConfirmationSchema
