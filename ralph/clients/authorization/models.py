import uuid

from django.db import models
from django.utils.timezone import now


class User(models.Model):

    """
    Model for user entries.

    This class models database table to store user information.

    Attributes:
        uuid (object): VARCHAR column to store user unique identifier.
        username (object): VARCHAR column to store user username.
        password (object): VARCHAR column to store user password.
        email (object): VARCHAR column to store user email address.
        first_name (object): VARCHAR column to store user first name.
        last_name (object): VARCHAR column to store user last name.
        is_active (object): BOOLEAN column to store information if user is active.
        created (object): DATETIME column to store date of user creation.
        updated (object): DATETIME column to store date of user last updated.
        roles (object): MANYTOMANY relation between user table and role table.
    """

    uuid = models.CharField(
        max_length=40, primary_key=True, default=uuid.uuid4, null=False
    )
    username = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=False, null=False)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)

    roles = models.ManyToManyField(to="Role")

    class Meta:
        db_table = "users"


class Role(models.Model):

    """
    Model for user roles entries.

    This class models database table to store user roles information.

    Attributes:
        id (object): INTEGER column with auto increment used as role id.
        name (object): VARCHAR column to store name of role.
        description (object): VARCHAR column to store basic description of the role.
        created (object): DATETIME column to store date of role creation.
        updated (object): DATETIME column to store date of role last updated.
        permissions (object): MANYTOMANY relation between role table and permission
            table.
    """

    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=150, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)

    permissions = models.ManyToManyField(to="Permission")

    class Meta:
        db_table = "roles"


class Permission(models.Model):

    """
    Model for role permissions entries.

    This class models database table to store role permissions information.

    Attributes:
        id (object): INTEGER column with auto increment used as permission id.
        name (object): VARCHAR column to store name of permission.
        created (object): DATETIME column to store date of permission creation.
        updated (object): DATETIME column to store date of permission last updated.
        description (object): VARCHAR column to store basic description of the
            permission.
    """

    name = models.CharField(max_length=50, null=False, primary_key=True)
    description = models.CharField(max_length=150, null=True)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)

    class Meta:
        db_table = "permissions"
