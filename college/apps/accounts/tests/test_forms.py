from django.test import TestCase
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.accounts.admin_forms import UserCreationForm, UserChangeForm
from apps.accounts.models import User


class UserCreationFormTestCase(TestCase):
    def setUp(self):
        self.form = UserCreationForm(data={
            "phone_number": "4047241937",
            "email": "uservaliddata@gmail.com",
            "password1": ">PvkqdX@",
            "password2": ">PvkqdX@"
        })

    def test_form_valid_data(self):
        """
        Tests the data validation of form.
        Sent the validate data to the form and checks
        the result of 'form.is_valid' to ensure 'True' assertion.
        """
        self.assertTrue(self.form.is_valid())

    def test_form_invalid_data(self):
        """
        Tests the invalidated data of form.
        Sent the invalid data to the form and checks
        the result of 'form.is_valid' to ensure 'False' assertion.
        """
        form = UserCreationForm(data={
            "phone_number": "4047241937",
            "email": "uservaliddata",
            "password1": ">PvkqdX@",
            "password2": ">PvkqdX@"
        })
        self.assertFalse(form.is_valid())

    def test_form_nodata(self):
        """
        Ensure the False result of 'form.is_valid()'
        when sent no data (empty) to the form.
        """
        form = UserCreationForm(data={})

        self.assertFalse(form.is_valid())

    def test_password_mismatch(self):
        """
        Tests the passwords mismatch validation.
        Sent different password2 and test that
        the 'form.is_valid' returns False.
        """
        form = UserCreationForm(data={
            "phone_number": "4047241937",
            "email": "uservaliddata",
            "password1": ">PvkqdX@",
            "password2": ">PvkqdX!"
        })

        self.assertFalse(form.is_valid())

    def test_hashed_password(self):
        """
        Tests that the user creating using forms hashed password correctly.
        Gets the created user (the user created in setUp with form) and checks
        its password hashed with 'check_password' and direct password with '.password'.
        """
        self.form.save()
        user = User.objects.get(phone_number="+14047241937")

        self.assertTrue(user.check_password(">PvkqdX@"))
        self.assertNotEqual(user.password, ">PvkqdX@")

    def test_false_commit(self):
        """
        Tests whether the user created after setting False commit to 'form.save'.
        """
        user = self.form.save(commit=False)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(phone_number="+14047241937")

        # Checks if the user data saved correctly
        self.assertTrue(user.check_password(">PvkqdX@"))
        self.assertNotEqual(user.password, ">PvkqdX@")


class UserChangeFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="+14047241937",
            email="richiepagard@gmail.com",
            password=">PvkqdX@"
        )
        self.form = UserChangeForm(instance=self.user)

    def test_existing_values(self):
        """
        Tests if the form gets the sent instance values and initialized them.
        """
        phone_number = self.form.initial.get("phone_number")
        email = self.form.initial.get("email")

        self.assertEqual(phone_number, "+14047241937")
        self.assertEqual(email, "richiepagard@gmail.com")

    def test_password_read_only(self):
        """
        Tests that the user's password is displayed as a read-only
        password hash field in the change form.
        """

        self.assertIn("password", self.form.fields)
        self.assertIsInstance(
            self.form.fields.get("password"),
            ReadOnlyPasswordHashField
        )
        self.assertEqual(self.form.initial.get("password"), self.user.password)

    def test_change_phone_number(self):
        """
        Tests the phone number changing value frm the form
        of the created user in setUp to ensure the user returns new phone number.
        """
        form = UserChangeForm(
            instance=self.user,
            data={
                "phone_number": "+14047241940",
                "email": self.user.email,
                "is_active": self.user.is_active,
                "is_admin": self.user.is_admin,
                "is_staff": self.user.is_staff,
            }
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.user.refresh_from_db()
        self.assertEqual(str(self.user.phone_number), "+14047241940")

    def test_change_email(self):
        """
        Tests the email changing value frm the form
        of the created user in setUp to ensure the user returns new email.
        """
        form = UserChangeForm(
            instance=self.user,
            data={
                "phone_number": self.user.phone_number,
                "email": "richiepagard@yahoo.com",
                "is_active": self.user.is_active,
                "is_admin": self.user.is_admin,
                "is_staff": self.user.is_staff,
            }
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.user.refresh_from_db()
        self.assertEqual(str(self.user.email), "richiepagard@yahoo.com")

    def test_change_permissions_status(self):
        """
        Tests that is_active, is_admin, and is_staff can be changed
        through the user change form.
        """
        form = UserChangeForm(
            instance=self.user,
            data={
                "phone_number": self.user.phone_number,
                "email": self.user.email,
                "is_active": False,
                "is_admin": True,
                "is_staff": True,
            }
        )

        self.assertTrue(form.is_valid())
        form.save()

        self.user.refresh_from_db()

        self.assertFalse(self.user.is_active)
        self.assertTrue(self.user.is_admin)
        self.assertTrue(self.user.is_staff)

    def test_changing_email_does_not_change_password(self):
        """
        Tests that changing an ordinary user field does not modify
        the existing password hash.
        """
        password = ">PvkqdX@"
        original_password_hash = self.user.password

        form = UserChangeForm(
            instance=self.user,
            data={
                "phone_number": self.user.phone_number,
                "email": "richiepagard@yahoo.com",
                "is_active": self.user.is_active,
                "is_admin": self.user.is_admin,
                "is_staff": self.user.is_staff,
            },
        )

        self.assertTrue(form.is_valid())
        form.save()

        self.user.refresh_from_db()

        self.assertEqual(self.user.password, original_password_hash)
        self.assertTrue(self.user.check_password(password))
