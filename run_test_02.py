# -*- coding: utf-8 -*-

"""
Tests for Task 2
"""

from tasks import multiprocessing_search, get_files, get_keywords


if __name__ == "__main__":
    result, processing_time = multiprocessing_search(get_files(), get_keywords())
    for keyword, files in result.items():
        print(f"\nKeyword \"{keyword}\" found in files:\n{"\n".join([file for file in files])}")

    print(f"\nThe search was completed in {processing_time:.6f} seconds.")
