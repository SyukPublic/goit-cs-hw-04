# -*- coding: utf-8 -*-

"""
Generate the test data for Tasks
"""

from tasks import test_data_generate


if __name__ == "__main__":
    test_data_generate(keywords_count=10, files_count=100)
    print(f"The test data generated.")
