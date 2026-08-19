from django.db.models import Manager


class ActiveStudentsManager(Manager):
    """
    Manager to filter all the active students.
    The filter only checks whether the 'is_active' is True or False.
    """

    def get_queryset(self):

        return super().get_queryset().filter(is_active=True)
