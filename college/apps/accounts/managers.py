from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation and superuser creation.
    This manager provides methods to create users with a phone number and email,
    ensuring that both fields are provided and valid. It also normalizes the email
    to prevent inconsistencies that could lead to security vulnerabilities.

    Methods:
        create_user(phone_number, email, password).
        create_superuser(phone_number, email, password).
    """
    def create_user(self, phone_number, email, password=None):
        """
        Creating a regular user with the provided phone number, email, and password.
        This method checks for the presence of both phone number and email, raising
        a ValueError if either is missing. It also normalizes the email to ensure
        consistency and security.

        Arguments:
            phone_number (str): The user's phone number.
            email (str): The user's email address.
            password (str, optional): The user's password. Defaults to None.
        """
        if not phone_number:
            raise ValueError(_("User must have a phone number."))
        if not email:
            raise ValueError(_("User must have an email address."))

        user = self.model(
            phone_number=phone_number,
            # Normalize email to prevent inconsistencies that could lead to `unkind` attacks,
            # where different variations of an email might bypass security checks.
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone_number, email, password=None):
        """
        Creating the superuser with the provided phone number, email, and password.
        This method ensures that the superuser has the necessary permissions and attributes 
        set for administrative tasks.

        Arguments:
            phone_number (str): The superuser's phone number.
            email (str): The superuser's email address.
            password (str, optional): The superuser's password. Defaults to None.
        """
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
