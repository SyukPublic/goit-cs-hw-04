# -*- coding: utf-8 -*-"

"""
Functions for generate the test data for tasks
"""

from faker import Faker
from pathlib import Path
from typing import Union

from .file import get_absolute_path


def generate_keywords(n: int = 30, file: Union[Path, str] = "keywords.txt") -> None:
    """
    Generates n random words in Ukrainian and English and writes them to a file.

    :param n: Number of random words
    :param file: The file where the generated words will be saved
    """
    fake_ua = Faker("uk_UA")
    fake_en = Faker("en_US")

    Path(file).write_text(
        ", ".join([fake_ua.word() if i % 2 != 0 else fake_en.word() for i in range(n)]),
        encoding="utf-8",
    )


def generate_text_files(n: int = 30, folder: Union[Path, str] = "__data__") -> None:
    """
    Generates n files with randomly generated phrases in Ukrainian and English and saves them in the specified folder.

    :param n: Number of files
    :param folder: The folder where the generated files will be saved
    """
    fake_ua = Faker("uk_UA")
    fake_en = Faker("en_US")

    Path(folder).mkdir(exist_ok=True)
    for i in range(1, n + 1):
        text = "\n".join(fake_ua.paragraphs(nb=50) if i % 2 != 0 else fake_en.paragraphs(nb=50))
        get_absolute_path(folder / f"text_{i:05d}.txt").write_text(text, encoding="utf-8")


def test_data_generate(keywords_count: int = 10, files_count: int = 100) -> None:
    """
    Generates a set of fake data for tasks.

    :param keywords_count: Number of keywords for the search
    :param files_count: Number of files to search through
    """
    generate_keywords(n=keywords_count, file=get_absolute_path(Path(__file__).parent / "./__data__/keywords.txt"))
    generate_text_files(n=files_count, folder=get_absolute_path(Path(__file__).parent / "./__data__/"))
