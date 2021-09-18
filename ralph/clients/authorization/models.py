import uuid

from django.db.models import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    ManyToManyField,
    Model,
)
from django.utils.timezone import now


class User(Model):

    """
    Model for user entries.

    This class models database table to store user information.

    Attributes:
        user_uuid (CharField): VARCHAR column to store user unique identifier.
        username (CharField): VARCHAR column to store user username.
        password (CharField): VARCHAR column to store user password.
        email (CharField): VARCHAR column to store user email address.
        first_name (CharField): VARCHAR column to store user first name.
        last_name (CharField): VARCHAR column to store user last name.
        is_active (BooleanField): BOOLEAN column to store information if user is active.
        created (DateTimeField): DATETIME column to store date of user creation.
        updated (DateTimeField): DATETIME column to store date of user last updated.
        roles (ManyToManyField): MANYTOMANY relation between user table and role table.
    """

    user_uuid = CharField(
        max_length=40,
        primary_key=True,
        default=uuid.uuid4,
        null=False,
        db_column="uuid",
    )
    username = CharField(max_length=30, null=False, unique=True)
    password = CharField(max_length=100, null=False)
    email = CharField(max_length=100, null=False)
    first_name = CharField(max_length=50, null=False)
    last_name = CharField(max_length=50, null=False)
    is_active = BooleanField(default=False, null=False)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)

    roles = ManyToManyField(to="Role")

    class Meta:
        db_table = "users"


class Role(Model):

    """
    Model for user roles entries.

    This class models database table to store user roles information.

    Attributes:
        id (AutoField): INTEGER column with auto increment used as role id.
        name (CharField): VARCHAR column to store name of role.
        description (CharField): VARCHAR column to store basic description of the role.
        created (DateTimeField): DATETIME column to store date of role creation.
        updated (DateTimeField): DATETIME column to store date of role last updated.
        permissions (ManyToManyField): MANYTOMANY relation between role table and
            permission table.
    """

    id = AutoField(primary_key=True)
    name = CharField(max_length=50, unique=True, null=False)
    description = CharField(max_length=150, null=True)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)

    permissions = ManyToManyField(to="Permission")

    class Meta:
        db_table = "roles"


class Permission(Model):

    """
    Model for role permissions entries.

    This class models database table to store role permissions information.

    Attributes:
        id (AutoField): INTEGER column with auto increment used as permission id.
        name (CharField): VARCHAR column to store name of permission.
        created (CharField): DATETIME column to store date of permission creation.
        updated (DateTimeField): DATETIME column to store date of permission last
            updated.
        description (DateTimeField): VARCHAR column to store basic description of the
            permission.
    """

    id = AutoField(primary_key=True)
    name = CharField(max_length=50, null=False, unique=True)
    description = CharField(max_length=150, null=True)
    created = DateTimeField(default=now)
    updated = DateTimeField(default=now)

    class Meta:
        db_table = "permissions"
