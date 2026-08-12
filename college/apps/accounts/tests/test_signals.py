from django.test import TestCase

from apps.accounts.models import User, UserProfile


class UserSignalTestCase(TestCase):

    def test_user_creation_creates_profile(self):
        """
        Tests that creating a User automatically creates a UserProfile
        associated with that User.
        """
        user = User.objects.create_user(
            phone_number="+14047241937",
            email="richiepagard@gmail.com",
        )
        profile = UserProfile.objects.get(user=user)

        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, user)

    def test_user_update_does_not_create_profile(self):
        """
        Tests that saving an existing User does not create another UserProfile.
        """
        user = User.objects.create_user(
            phone_number="+14047241937",
            email="richiepagard@gmail.com",
        )
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

        user.email = "richiepagard@example.com"
        user.save()

        self.assertEqual(UserProfile.objects.filter(user=user).count(), 1)

    def test_user_save_saves_profile(self):
        """
        Tests that saving a User also saves its associated UserProfile.
        """
        user = User.objects.create_user(
            phone_number="+14047241937",
            email="richiepagard@gmail.com",
        )
        profile = user.profile
        profile.firstname = "Richie"

        user.save()
        profile.refresh_from_db()

        self.assertEqual(profile.firstname, "Richie")
