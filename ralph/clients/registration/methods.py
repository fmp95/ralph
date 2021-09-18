from typing import Any, Dict

from bcrypt import hashpw, gensalt
from django.forms.models import model_to_dict
from ralph.clients.authorization.models import User
from ralph.clients.registration.schemas import RegistrationSchema
from ralph.common.exceptions import ValidationException
from ralph.common.logger import get_logger

logger = get_logger(__name__)


def register_user(data: RegistrationSchema) -> Dict[str, Dict[str, Any]]:

    """
    Register new user to database.

    This function checks if user has correct information to register and if so register
    it.

    Args:
        data (RegistrationSchema): Information passed for registring a new user.

    Return:
        Dict[str, Dict[str, Any]]: Information on created user.
    """

    # Get user info as dict.
    user_info = data.dict().copy()

    # Check if username is in use.
    if User.objects.filter(username=user_info["username"]).exists():
        raise ValidationException("Username already in use.")

    # Remove user unnecessary information.
    user_info.pop("terms_accepted")
    user_info.pop("password_confirm")

    # Hashes password
    user_info.update({"password": hash_password(user_info["password"])})

    # Create new user instace and save to database
    new_user = User.objects.create(**user_info)
    new_user.save()

    logger.info("User created with information: %s.", user_info)

    return {"data": model_to_dict(new_user)}


def hash_password(password: str) -> str:

    """
    Hashes password using bcrypt.

    Args:
        password (str): User's password.

    Returns:
        str: Hashed password.
    """

    return str(hashpw(password.encode(), gensalt()).decode())
