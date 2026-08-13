import os

from django.test import SimpleTestCase

from apps.common.utils import path_with_hash


class PathWithHashTestCase(SimpleTestCase):

    def test_preserves_path_and_extension(self):
        """
        Tests that the original directory, filename, and file extension
        are preserved in the generated path.
        """
        result = path_with_hash("avatars/profile.jpg")

        directory, filename = os.path.split(result)
        root, extension = os.path.splitext(filename)

        self.assertEqual(directory, "avatars")
        self.assertTrue(root.startswith("profile_"))
        self.assertEqual(extension, ".jpg")

    def test_generates_seven_character_random_suffix(self):
        """
        Tests that the generated filename contains a seven-character
        random suffix.
        """
        result = path_with_hash("profile.jpg")

        filename = os.path.basename(result)
        root, _ = os.path.splitext(filename)

        random_part = root.removeprefix("profile_")

        self.assertEqual(len(random_part), 7)

    def test_generates_different_paths(self):
        """
        Tests that repeated calls generate different randomized paths.
        """
        first = path_with_hash("profile.jpg")
        second = path_with_hash("profile.jpg")

        self.assertNotEqual(first, second)
