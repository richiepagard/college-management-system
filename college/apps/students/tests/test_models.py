from django.test import TestCase
from django.db.utils import IntegrityError
from django.db import transaction
from django.contrib.auth import get_user_model

from apps.students.models import Student

User = get_user_model()


class StudentTestCase(TestCase):
    def setUp(self):
        """
        Creates instances from User to test in various scenarios.
        """
        self.richie = User.objects.create_user(
            phone_number="+1-404-724-1937",
            email="richiepagard@gmail.com"
        )
        self.profile = self.richie.profile
        self.student = Student.objects.create(user=self.richie)

    def test_getting_student(self):
        """Tests the existence of student by getting created user in setUp."""
        student = Student.objects.get(user=self.richie)

        self.assertTrue(student.is_active)

    def test_student_one_to_one_relationship(self):
        """
        Tests that the user can only have one Student profile.
        """

        with self.assertRaises(IntegrityError):

            # Nested transaction to avoid TransactionManagementError
            with transaction.atomic():
                Student.objects.create(user=self.richie)

    def test_user_set_null_deletion(self):
        """
        Tests that if a user deleted, the user field in the Student model
        set to the NULL.
        """

        user = User.objects.create_user(
            phone_number="9096133866",
            email="usersetnull@gmail.com"
        )
        student = Student.objects.create(
            user=user,
            student_code="0123456789"
        )
        # Deletes the created user
        user.delete()
        student.refresh_from_db()

        self.assertIsNone(student.user)

    def test_student_code_uniqueness(self):
        """
        Tests the student code uniqueness.
        Gets the created user 'student code' which created in setUp,
        then creates a new student with a new user and set its studen code
        to the created student code in the setUp.
        Checks whether the IntegrityError raised or not.
        """
        duplicated_code = self.student.student_code

        user = User.objects.create_user(
            phone_number="9096133866",
            email="newuser@gmail.com"
        )
        user.save()
        student = Student.objects.create(user=user)
        student.student_code = duplicated_code

        with self.assertRaises(IntegrityError):
            student.save()

    def test_student_str_representation(self):
        """
        Tests the string representation of the Student, ensuring that it returns
        the expected format combining user's profile username(or phone number if that's None)
        and student code.
        Format: <user's username> (<student-code>)

        Saves objects in various formats and test the object str().
        """
        student_code = self.student.student_code
        # Tests the exists student with no username
        self.assertEqual(str(self.student), f"+14047241937 ({student_code})")

        # Set a username for the student and check with exists username, again
        self.profile.username = "RichiePagard"
        self.profile.save()
        self.assertEqual(str(self.student), f"richiepagard ({student_code})")
