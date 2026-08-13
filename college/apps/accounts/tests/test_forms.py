from django.test import TestCase

from apps.accounts.admin_forms import UserCreationForm
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
