from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents a user in the system. Default user model.

    Attributes:
        phone_number (PhoneNumberField): The user's phone number, unique and required.
        email (EmailField): The user's email address, unique and required.
        is_active (BooleanField): Indicates whether the user account is active.
        is_admin (BooleanField): Indicates whether the user has admin privileges.
    """
    phone_number = PhoneNumberField(
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        verbose_name=_("Phone Number")
    )
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        verbose_name=_("E-mail")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Staff Status")
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name=_("Admin")
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


    def __str__(self) -> str:
        """
        Return a string representation of the user.
        """
        return f"{self.phone_number} - {self.email}"
