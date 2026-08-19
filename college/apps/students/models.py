from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.common.models import BaseModel
from apps.common.utils import unique_code_generator

User = get_user_model()


class Student(BaseModel):
    """
    Represents to the Student's in the college.
    Each student is like a user with Student role.

    Attributes:
        user (int, O2O): The student's user. Implies to the user and its profile.
        student_code (str): Student's unique code with '10' length to identify each student by the code.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="student",
        null=True,
        verbose_name=_("User")
    )
    student_code = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        blank=True,
        verbose_name=_("Student Code")
    )

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self) -> str:
        return f"{self.user.phone_number} - {self.student_code}"

    def save(self, *args, **kwargs) -> None:
        """
        Overriding the save method.
        If the target object is new, then generates an unique code
        for the student's Student Code field.
        """
        is_new = self.pk is None

        if is_new:
            self.student_code = unique_code_generator(10)

        super().save(*args, **kwargs)
