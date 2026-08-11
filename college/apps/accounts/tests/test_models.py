from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction

from apps.accounts.models import User


class UserTestCase(TestCase):
    def setUp(self):
        """
        Creates instances from User to test in various scenarios.
        """
        self.brad = User.objects.create_user(
            phone_number="418-543-8090",
            email="bradfortest@yahoo.com"
        )
        self.tommy = User.objects.create_user(
            phone_number="+1-587-530-2271",
            email="tommyfortest@gmail.com"
        )
        self.richie = User.objects.create_user(
            phone_number="+1-404-724-1937",
            email="richiepagard@gmail.com"
        )

        User.objects.create_user(
            phone_number="+1-623-416-0089",
            email="nothingatstake@empty.com"
        )
        User.objects.create_user(
            phone_number="+1-343-528-0149",
            email="djangounchained@cool.net"
        )

    def test_user_phone_number(self):
        """
        Checks whether the created user in setUp
        has the correct phone number format.
        """
        self.assertEqual(str(self.brad.phone_number), "+14185438090")
        self.assertEqual(str(self.tommy.phone_number), "+15875302271")
        self.assertEqual(str(self.richie.phone_number), "+14047241937")

    def test_user_not_equal_phone_number(self):
        """
        Checks if the created user in setUp
        has incorrect phone number format.
        """
        self.assertNotEqual(str(self.brad.phone_number), "4185438090")
        self.assertNotEqual(str(self.tommy.phone_number), "15875302271")
        self.assertNotEqual(str(self.richie.phone_number), "+1-404-724-1937")

    def test_user_existence(self):
        """
        Gets users those just created simply in setUp with no variables
        and tests the existence of the users by the user activation status,
        if the 'is_active' True, the user created successfully because the default
        value of 'is_active' is True in models.
        """
        nas = User.objects.get(phone_number="+16234160089")
        django_unchained = User.objects.get(email="djangounchained@cool.net")

        self.assertTrue(nas.is_active)
        self.assertTrue(django_unchained.is_active)

    def test_user_does_not_exist(self):
        """
        Tied to gets an user object that does not exist in the db
        because it has never created.
        """
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(phone_number="+18255423622")

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email="richiepagard@yahoo.com")

    def test_user_uniqueness(self):
        """
        Creates a new user with exist data and
        Tests whether the user already exists or not.
        """
        with self.assertRaises(IntegrityError):

            # Nested transaction to avoid TransactionManagementError
            with transaction.atomic():
                User.objects.create_user(
                    phone_number="+18255423623",
                    email="richiepagard@gmail.com",
                    password=">PvkqdX@"
                )

        with self.assertRaises(IntegrityError):

            # Nested transaction to avoid TransactionManagementError
            with transaction.atomic():
                User.objects.create_user(
                    phone_number="+14047241937",
                    email="thiisjustforfun@gmail.com",
                    password=">PvkqdX@"
                )

    def test_user_permission(self):
        """
        Tests created users / instances in setUp for their permission,
        if 'is_admin', 'is_staff', or 'is_superuser' are False, means
        the created users are not admin and contain normal permissions.
        """
        self.assertFalse(self.brad.is_admin)
        self.assertFalse(self.brad.is_staff)
        self.assertFalse(self.brad.is_superuser)

        self.assertFalse(self.tommy.is_admin)
        self.assertFalse(self.tommy.is_staff)
        self.assertFalse(self.tommy.is_superuser)

        self.assertFalse(self.richie.is_admin)
        self.assertFalse(self.richie.is_staff)
        self.assertFalse(self.richie.is_superuser)

    def test_user_creation_validation(self):
        """
        Tests the validation of user creation by checking for missing
        required fields such as phone number and email. If either field is missing,
        a ValueError should be raised, indicating that the user cannot be created without
        these essential attributes. This test ensures that the user creation process
        adheres to the defined constraints and maintains data integrity.
        """
        with self.assertRaises(ValueError):

            # Nested transaction to avoid TransactionManagementError
            with transaction.atomic():
                User.objects.create_user(
                    phone_number="",
                    email="cbum@gmail.com"
                )

        with self.assertRaises(ValueError):
        
            # Nested transaction to avoid TransactionManagementError
            with transaction.atomic():
                User.objects.create_user(
                    phone_number="+15562100010",
                    email=""
                )

        with self.assertRaises(ValueError):
                
            # Nested transaction to avoid TransactionManagementError
            with transaction.atomic():
                User.objects.create_user(
                    phone_number=None,
                    email="cbum@yahoo.com"
                )

    def test_email_normalization(self):
        """
        Tests the normalization of email addresses during user creation.
        E-mail normalization handles in managers and ensures that created user email address
        stored in correct format.
        """
        user = User.objects.create_user(
            phone_number="+15562100011",
            email="RICHIESTUDIO@GMAIL.COM"
        )
        self.assertEqual(user.email, "richiestudio@gmail.com")

    def test_user_password_validation(self):
        """
        Tests the password validation for the created user,
        ensuring that the password is correctly set and can be verified.
        """
        user = User.objects.create_user(
            phone_number="+15562100012",
            email="cbum@gmail.com",
            password=">PvkqdX@"
        )
        user_no_password = User.objects.create_user(
            phone_number="+15562100013",
            email="robert@gmail.com"
        )

        self.assertTrue(user.check_password(">PvkqdX@"))
        self.assertFalse(user.check_password("wrongpassword"))
        self.assertFalse(user_no_password.has_usable_password())

    def test_create_superuser(self):
        """
        Tests the creation of a superuser, ensuring that the user has the correct
        permissions and attributes set for administrative tasks.
        """
        user = User.objects.create_superuser(
            phone_number="+14155550000",
            email="superuser@yahoo.com",
            password=">PvkqdX@"
        )

        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_superuser)

    def test_user_str_representation(self):
        """
        Tests the string representation of the user, ensuring that it returns
        the expected format combining phone number and email.
        """
        self.assertEqual(str(self.brad), "+14185438090 - bradfortest@yahoo.com")
