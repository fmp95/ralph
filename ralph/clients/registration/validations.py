from typing import Dict, Any

from ralph.common.exceptions import ValidationException
from ralph.common.logger import get_logger

logger = get_logger(__name__)


def validates_password_format(password: str) -> str:

    """
    Validates if password checks all rules required.

    Every password should have between 8 and 20 characters, at least one special
    character, at least one uppercase character and at least one numeric character to
    be valid.

    Args:
        password (str): User's desired password.

    Returns:
        str: User's desired password.

    Raises:
        ValidationException: If password don't check all rules.
    """

    # Rules for password validation
    rules = {
        "special_character": False,
        "uppercase_character": False,
        "numeric_character": False,
        "no_space": ...,
    }

    # Password length
    password_length = len(password)

    # Check if password length is correct
    if not password_length >= 8 and not password_length <= 20:
        raise ValidationException("Password should have between 8 and 20 characters.")

    # Check each character of password
    for character in password:

        # Check if is special character and approve rule.
        if not rules["special_character"] and not character.isalnum():
            rules["special_character"] = True

        # Check if is uppercase character and approve rule.
        if not rules["uppercase_character"] and character.isupper():
            rules["uppercase_character"] = True

        # Check if is numeric character and approve rule.
        if not rules["numeric_character"] and character.isnumeric():
            rules["numeric_character"] = True

        # Check if is a space character.
        if rules["no_space"] and character == " ":
            rules["no_space"] = False

    # If any rule is not checked, raise ValidationError.
    if not all(rules.values()):

        logger.info("Password doesn't match rules.")
        logger.info("Rules: %s.", rules)

        raise ValidationException(
            "Password should have a special character, an uppercase character, "
            + "a numeric character and no space."
        )

    return password


def check_same_password(password_confirm: str, values: Dict[str, Any]) -> str:

    """
    Checks if password and password confirmation matches.

    Args:
        password_confirm (str): Password confirmation provided.
        values (Dict[str, Any]): Other values passed in object.

    Returns:
        str: Password confirmation value.

    Raises:
        ValidationException: If passwords don't match or password value is not passed.
    """

    # Checks if password field exists.
    if not "password" in values:
        raise ValidationException("A password should be passed.")

    # Check if passwords are equal.
    if not password_confirm == values["password"]:
        raise ValidationException("Passwords should be equal.")

    return password_confirm


def validates_username_format(username: str) -> str:

    """
    Validates username format.

    Username should have length greater than 5 and lower or equal to 30, all lowercase
    and have no spaces.

    Args:
        username (str): Username value.

    Returns:
        str: Username value.
    """

    # Username length.
    username_length = len(username)

    # Check if username length is correct.
    if not username_length > 5 and username_length <= 30:
        raise ValidationException(
            "Username should have more than 5 character and up to 30 characters."
        )

    # Rules that username should follow.
    rules = {
        "all_lowercase": ...,
        "no_space": ...,
    }

    # Check each character of username.
    for character in username:

        # Check if is not a lowercase character.
        if rules["all_lowercase"] and character.isalpha() and not character.islower():
            rules["all_lowercase"] = False

        # Check if is a space character.
        if rules["no_space"] and character == " ":
            rules["no_space"] = False

    # If any rule is not checked, raise ValidationError.
    if not all(rules.values()):

        logger.info("Username doesn't match rules.")
        logger.info("Rules: %s.", rules)

        raise ValidationException(
            "Username should have length greater than 5 and lower or equal to 30, "
            + "all lowercase and have no spaces."
        )

    return username
