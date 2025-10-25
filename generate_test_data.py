# -*- coding: utf-8 -*-

"""
Generate the test data for Tasks
"""

import argparse

from tasks import test_data_generate


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates a set of fake keywords and text files",
        epilog="Good bye!",
    )
    parser.add_argument("-k", "--keywords", type=int, default=10, help="Number of keywords")
    parser.add_argument("-f", "--files", type=int, default=100, help="Number of files")

    args = parser.parse_args()

    test_data_generate(keywords_count=args.keywords, files_count=args.files)
    print(f"The test data generated.")
