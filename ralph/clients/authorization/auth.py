from typing import List, Dict, TypedDict

from django.http import HttpRequest
from jose import JWTError, jwt
from ninja.security import HttpBearer

from ralph.clients.authorization.models import Role, User
from ralph.common.exceptions import InvalidTokenException, UnauthorizedException
from ralph.common.logger import get_logger
from settings import JWT_ALGORITHM, JWT_SECRET

logger = get_logger(__name__)


class AuthorizationResponse(TypedDict):

    """
    Structure of authorization response.

    This class shows the types expected for the dictionary response of authorization.

    Attributes:
        uuid (str): User's unique identifier.
        username (str): User's username.
        first_name (str): User's first name..
        last_name (str): User's last name.
        email (str): User's e-mail address.
        is_active (bool): Boolean that represents if user is active in system.
        roles (List[str]): List containing name of every user's roles.
        permissions (List[str]): List containing name of every user's permissions, based
            on its roles.
    """

    uuid: str
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    roles: List[str]
    permissions: List[str]


class Authorization(HttpBearer):

    """
    Handles authorization to request and access contents based on configuration.

    This class manages authorization to access content based on three types of
    information: token, role and permission. The main check is done to the bearer
    token passed in the header, checking if the token is valid. If so, the class can
    also check if the token user has any specified role or permission, passed as
    arguments when class is set as a parameter to the endpoint parameter auth.

    Most of the configurations are inherited from HttpBearer class, from Django Ninja.
    """

    def __init__(self, roles: List[str] = None, permissions: List[str] = None) -> None:

        """
        Constructor to authorization class.

        This class constructs from HttpBearer class, from Django Ninja, and do extra
        configuration to handles roles and permissions access.

        Args:
            roles (List[str]): List of roles that can access endpoint. User must have
                at least one of those roles. Defaults to None.
            permissions (List[str]): List of permissions that is necessary to access
                endpoint. User must have at least one of those permissions. Defaults to
                None.

        Returns:
            None
        """

        super().__init__()

        # Set passed roles as instance parameter.
        self.roles = roles or []

        # Set passed permissions as instance parameter.
        self.permissions = permissions or []

    def authenticate(self, request: HttpRequest, token: str) -> AuthorizationResponse:

        """
        Authenticate access based on configuration passed to constructor.

        This method is called to authenticate access, based on the information sent
        to instance constructor.

        Args:
            request (HttpRequest): Object containing request information.
            token (str): Bearer token passed via header.

        Returns:
            dict: Information on the user requesting access, such as username, roles and
                permissions.
        """

        logger.info("Protected endpoint: %s.", request.path)

        logger.info(
            "Required roles: %s (Any) | Required permissions: %s (Any).",
            self.roles,
            self.permissions,
        )

        # Try to decode passed token.
        decoded_token = self.decode_token(token)

        # Retrieve UUID from payload.
        user_uuid = decoded_token.get("iss")

        logger.info("User uuid: %s.", user_uuid)

        # Try to get user object from UUID.
        user = self.get_user(user_uuid)

        # Get roles from user.
        user_roles = self.get_user_roles(user)

        # Get permission from user.
        user_permissions = self.get_user_permissions(user_roles)

        # Creates an object with authorization checking.
        authorizations = {
            "roles": any(role in self.roles for role in user_roles)
            if self.roles
            else True,
            "permissions": any(
                permission in self.permissions for permission in user_permissions
            )
            if self.permissions
            else True,
        }

        logger.info("Authorizations: %s.", authorizations)

        # If any authorization isn't met, raises unauthorized expection.
        if not all(authorizations.values()):
            logger.warning("User doesn't have necessary authorization.")
            raise UnauthorizedException("User doesn't have necessary authorization.")

        return AuthorizationResponse(
            uuid=decoded_token.get("iss"),
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            roles=user_roles,
            permissions=user_permissions,
        )

    @staticmethod
    def decode_token(token: str) -> Dict[str, str]:

        """
        Checks if token is valid and decodes it.

        This function tries to decode the passed token and also validates its
        authenticity.

        Args:
            token (str): Bearer token.

        Returns:
            Dict[str, str]: Payload information stored in token.
        """

        # Try to decode token.
        try:
            logger.info("Token is valid.")
            decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        except JWTError as exc:
            logger.warning("Token is not valid. Error: %s.", str(exc))
            raise InvalidTokenException("Token is not valid.") from exc

        return decoded_token

    @staticmethod
    def get_user(user_uuid: str) -> User:

        """
        Get user object from database.

        This function gets user entry in the database.

        Args:
            uuid (str): User uuid to filter entries.

        Returns:
            User: Object with user information.
        """

        # Try to get user object.
        try:
            return (
                User.objects.prefetch_related("roles").filter(user_uuid=user_uuid).get()
            )
        except User.DoesNotExist as exc:
            logger.warning("User doesn't exist.")
            raise InvalidTokenException("User doesnt' exist.") from exc

    @staticmethod
    def get_user_roles(user: User) -> List[str]:

        """
        Get user roles names.

        This function gets roles of user in the database and return a list of the
        name of all roles.

        Args:
            user (User):

        Returns:
            List[str]: List of role names.
        """

        # Retrieve user roles.
        user_roles = list(user.roles.values_list("name", flat=True).distinct())

        return user_roles

    @staticmethod
    def get_user_permissions(roles: List[str]) -> List[str]:

        """
        Get roles permission names.

        This function gets roles permissions in the database and return a list of the
        name of all permissions.

        Args:
            roles (List[str]): List of user roles names.

        Returns:
            List[str]: List of permissions names.
        """

        # Get user permissions.
        user_permissions = (
            Role.objects.prefetch_related("permissions")
            .filter(name__in=roles)
            .values_list("permissions__name", flat=True)
            .distinct()
        )

        # Use set to remove duplicates.
        return list(set(user_permissions))
