from django.db import models
from django.utils.translation import gettext_lazy as _

from .user import User
from apps.common.models import BaseModel
from apps.common.utils import path_with_hash


def avatar_path(instance, filename: str) -> str:
    """
    Uploads the user profile image file with a hash
    method to encrypting the file.
    """
    return f"userprofile/avatar/{path_with_hash(filename)}"


class UserProfile(BaseModel):
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
        avatar_image (file): The user profile picture.
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
    avatar_image = models.ImageField(
        upload_to=avatar_path,
        null=True,
        blank=True,
        verbose_name=_('Avatar Image')
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

    @property
    def fullname(self) -> str:
        """
        Returns the fullname of the user with filter.
        If the user has both first name and last name, it returns "Firstname Lastname".
        If the user has only first name, it returns "Firstname".
        If the user has only last name, it returns "Lastname".
        If the user has neither first name nor last name, it returns "Unknown".
        """
        fname = self.firstname if self.firstname else None
        lname = self.lastname if self.lastname else None

        if fname and lname:
            return f"{fname.title()} {lname.title()}"
        elif fname and not lname:
            return f"{fname.title()}"
        elif lname and not fname:
            return f"{lname.title()}"
        else:
            return "Unknown"
