from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User


class UserProfile(models.Model):
    """
    Represents a user profile associated with a user account.
    User profile contains additional information about the user, these information are optional
    but same for all the roles of users.

    Attributes:
        user (User): The user associated with this profile.
        username (str): The username of the user.
        firstname (str): The first name of the user.
        lastname (str): The last name of the user.
        national_code (str): The national code of the user.
        birth_date (date): The birth date of the user.
        address (str): The address of the user.
        created_at (datetime): The timestamp when the profile was created.
        updated_at (datetime): The timestamp when the profile was last updated.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("Username"),
    )
    firstname = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=_("First Name"),
    )
    lastname = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name=_("Last Name"),
    )
    national_code = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name=_("National Code"),
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Birth Date"),
    )
    address = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("Address"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
    )

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self) -> str:
        """
        Return the string representation of the user profile.
        """
        username = self.username or self.user.phone_number
        national_code = self.national_code or "N/A"

        return f"{username} ({national_code})"
