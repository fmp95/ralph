from datetime import datetime, timedelta

from bcrypt import checkpw
from jose import jwt

from ralph.clients.authorization.models import User
from ralph.common.exceptions import InvalidCredentialException
from ralph.common.logger import get_logger
from settings import JWT_ALGORITHM, JWT_SECRET, JWT_TIMEDELTA_IN_MINUTES

logger = get_logger(__name__)


def login(username: str, password: str) -> str:

    """
    Generates a bearer token if credentials are successful.

    Args:
        username (str): Requested username value of user trying to login.
        password (str): Password value to check against hash.

    Returns:
        str: Bearer token.
    """

    # Try to get user object from username.
    try:
        logger.info("Trying to get user with username: %s.", username)
        user = User.objects.filter(username=username).get()
    except User.DoesNotExist as exc:
        logger.warning("No user found with given username.")
        raise InvalidCredentialException from exc

    logger.info("User found. Checking password (No log if correct password).")

    # Check if password is correct.
    if not checkpw(password.encode(), user.password.encode()):
        logger.warning("Invalid password: %s", password)
        raise InvalidCredentialException

    return _generate_token(user.user_uuid)


def _generate_token(user_uuid: str) -> str:

    """
    Generates a bearer token.

    Args:
        username (str): User uuid to be added as issuer of token.

    Returns:
        str: Bearer token.
    """

    logger.info("Generating bearer token.")

    # Create payload for JWT token.
    payload = {
        "iss": user_uuid,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=JWT_TIMEDELTA_IN_MINUTES),
    }

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
