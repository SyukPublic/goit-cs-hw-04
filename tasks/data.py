# -*- coding: utf-8 -*-"

"""
Helper functions for works with the data for tasks
"""

import re
from pathlib import Path

from .file import get_absolute_path, load_text_file_data


def get_keywords() -> list[str]:
    """
    Get a list of keywords.

    :return: List of keywords
    """
    return [
        keyword.strip() for keyword in load_text_file_data(
            get_absolute_path(Path(__file__).parent / "./__data__/keywords.txt")
        ).split(",")
    ]

def get_files() -> list[Path]:
    """
    Get a list of files paths.

    :return: List of files paths
    """
    return [
        child for child in get_absolute_path(Path(__file__).parent / "./__data__/").iterdir()
        if child.is_file() and re.match(r"text_\d{2,5}.txt", child.name)
    ]


def split_files_evenly(seq: list[Path], n: int) -> list[list[Path]]:
    """
    Evenly divides the list of files paths into n parts.

    :param seq: List of files paths
    :param n: Parts count
    :return: List of list
    """
    k, m = divmod(len(seq), n)
    # The first m parts will be longer by one element.
    return [seq[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]
