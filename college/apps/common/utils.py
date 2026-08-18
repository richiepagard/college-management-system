import os
import string
from secrets import choice

from django.utils.crypto import get_random_string


def path_with_hash(name: str) -> str:
    """
    Encrypting the file upload with File or Image Fields
    or any other fields will use to uploading a file.

    Arguments:
        name (str): The file name will uploaded.
    """
    dir_name, file_name = os.path.split(name)
    file_root, file_ext = os.path.splitext(file_name)
    random = get_random_string(7)

    return os.path.join(dir_name, f"{file_root}_{random}{file_ext}")


def unique_code_generator(length: int = 10) -> str:
    """
    Generates a unique random code with provided length by function argument,
    which by defautl is 10.
    For the fields with '<role>-code' name, Student Code or Professor Code etc.
    The code contains only digits.

    Arguements:
        length (int): The length of the generated code.
    """
    digits = string.digits
    generated_code = "".join( choice(digits) for _ in range(length) )

    return generated_code
