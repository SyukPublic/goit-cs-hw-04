# -*- coding: utf-8 -*-"

"""
Functions for works with the files and directories
"""

from typing import Optional, Union
from pathlib import Path


def get_absolute_path(path: Union[Path, str], current_dir: Optional[Union[Path, str]] = None) -> Path:
    """
    Return the absolute path for the given path and the current directory.

    :param path: specified path (str, Path, mandatory)
    :param current_dir: current directory (str, Path, optional)
    :return: absolute path (Path)
    """
    if not path:
        # The path can not be None or an empty string
        raise ValueError("The path can not be empty")

    if Path(path).is_absolute():
        # If the specified path is an absolute - return it
        return Path(path)

    if current_dir is not None and isinstance(current_dir, str):
        # If the current directory is not specified, use the current working directory
        current_dir = Path(current_dir)

    # Construct an absolute path and return
    return (current_dir if current_dir is not None else Path.cwd()) / path


def load_text_file_data(file_path: Path, encoding: str = "utf-8") -> str:
    """
    Return the content of the given text file.

    :param file_path: specified text file path (Path, mandatory)
    :param encoding: encoding used to decode the file data (string, optional)
    :return: file content (string)
    """

    # Verify that the specified file exists
    if not file_path.exists():
        raise ValueError(f"The file \"{file_path}\" not found")

    # Verify that the specified path is the file
    if not file_path.is_file():
        raise ValueError(f"The specified path \"{file_path}\" is not a file")

    # Open the specified file as a text file
    try:
        with open(file_path, "tr", encoding=encoding) as fh:
            # Read the file data
            file_content = file_path.read_text(encoding=encoding)
            # Return the file data
            return file_content
    except UnicodeDecodeError:
        # The file data is corrupted
        # Raise exception to the upper level
        raise ValueError(f"The file \"{file_path}\" data is corrupted")
    except Exception as e:
        # An unexpected error occurred
        # Raise exception to the upper level
        raise Exception("An unexpected error occurred: {error}.".format(error=repr(e)))
