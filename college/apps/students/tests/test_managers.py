from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.students.models import Student

User = get_user_model()


class ActiveStudentsManagerTestCase(TestCase):
    def setUp(self):
        """
        Creates instances from User to test in various scenarios.
        """
        self.richie = User.objects.create_user(
            phone_number="+1-404-724-1937",
            email="richiepagard@gmail.com"
        )
        self.dennis = User.objects.create_user(
            phone_number="4047241938",
            email="dennis@gmail.com"
        )

        self.richie_student = Student.objects.create(user=self.richie)
        self.dennis_student = Student.objects.create(user=self.dennis)

        # Deactive the dennis student
        self.dennis.is_active = False
        self.dennis.save()

    def test_objects_activation_status(self):
        """
        Checks if the return objects / instances from the 'actives'
        manager, correctly filter the active students. Only True activations.

        Go through the list of 'Student.actives.all()' to check whether
        the return objects has True activation status.
        Gets the 'is_active' value from 'values_list' of queryset whcih returns a tuple
        contains the values of fields listed 'values_list', therefore, assertion per object (assertTrue).
        """
        students = Student.actives.all()

        for student in students.values_list("is_active"):
            for value in student:
                self.assertTrue(value)
