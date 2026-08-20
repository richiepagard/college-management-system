import os

from django.test import SimpleTestCase

from apps.common.utils import path_with_hash, unique_code_generator


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


class UniqueCodeGeneratorTestCase(SimpleTestCase):

    def test_return_string_digit_ensure(self):
        """
        Tests to ensure that the return string from
        the 'unique_code_generator' method is digit.
        """
        result = unique_code_generator(6)

        self.assertTrue(result.isdigit())
        self.assertFalse(result.isalpha())

    def test_correct_length_return(self):
        """
        Tests that the length of return string is exactly
        same as what passed to.
        """
        result = unique_code_generator(6)

        self.assertEqual(len(result), 6)

    def test_code_uniqueness(self):
        """
        Tests that the generated code is unique.
        """
        result1 = unique_code_generator(4)
        result2 = unique_code_generator(4)

        self.assertNotEqual(result1, result2)
        self.assertEqual(len(result1), len(result2))

    def test_default_length_value(self):
        """
        Testst that if pass nothing to the 'length'
        argument, it sets the default value which is '10'.
        """
        result = unique_code_generator()

        self.assertEqual(len(result), 10)
