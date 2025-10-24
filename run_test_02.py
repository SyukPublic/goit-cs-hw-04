# -*- coding: utf-8 -*-

"""
Tests for Task 2
"""

from tasks import multiprocessing_search, get_files, get_keywords


if __name__ == "__main__":
    result, processing_time = multiprocessing_search(get_files(), get_keywords())
    for keyword, files in result.items():
        print(f"Keyword \"{keyword}\" found in files:\n{"\n".join([file.as_posix() for file in files])}")

    print(f"The search was completed in {processing_time:.6f} seconds.")
