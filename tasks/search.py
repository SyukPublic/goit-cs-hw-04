# -*- coding: utf-8 -*-

"""
Search Engine for the tasks
"""

import logging
import sys
from multiprocessing import Queue
from pathlib import Path
from typing import Optional

from .boyer_moore import boyer_moore_search
from .file import load_text_file_data
from .logger import logger_init


class SearchEngine:
    sentinel = "__SEARCH_DONE__"

    def __init__(
            self,
            idx: int,
            files: list[Path],
            keywords: list[str],
            results_queue: "Queue[tuple[str, list[str]]]",
            thread: bool = False,
            logger: Optional[logging.Logger] = None,
    ):
        """
        Initialization of the search worker.

        :param idx: Worker index
        :param files: List of files in which keyword search will be performed
        :param keywords: List of keywords
        :param results_queue: Queue with worker search results
        :param thread: Flag indicating whether the worker is running as a thread
        :param logger: Logger instance (optional)
        """
        self.idx = idx

        self.files  = files
        self.keywords = keywords
        self.results_queue = results_queue

        self.thread = thread
        self.logger: Optional[logging.Logger] = logger

    def __call__(self, *args, **kwargs) -> None:
        """
        Searches for keywords in a set of files and writes the result to a queue.
        """
        try:
            # Initializes the logger if it hasn’t been initialized previously
            if self.logger is None:
                self.logger = logger_init(name=__name__, thread=self.thread)

            # Perform search
            for file in self.files:
                self.results_queue.put((file.as_posix(), self.search_keywords_in_file(file)))
        except Exception as e:
            self.logger.error(e)
        finally:
            self.results_queue.put((SearchEngine.sentinel, []))
            if not self.thread:
                sys.exit(0)


    def search_keywords_in_file(self, file: Path) -> list[str]:
        """
        Searches for keywords in a file and returns a list of found ones.

        :param file: The file in which the search must be performed
        :return: List of keywords found in the file
        """
        result: list[str] = []
        try:
            text: str = load_text_file_data(file)
            for keyword in self.keywords:
                if boyer_moore_search(text, keyword, find_all=False):
                    result.append(keyword)
        except Exception as e:
            self.logger.error(e)
        finally:
            self.logger.info(f"File \"{file.as_posix()}\" processed. Found keywords: {", ".join(result)}")
            return result


def collect_search_result(
        keywords: list[str],
        worker_numbers: int,
        results_queue: "Queue[tuple[str, list[str]]]"
) -> dict[str, list[str]]:
    """
    Collect the search results.

    :param keywords: List of keywords
    :param worker_numbers: Number of workers
    :param results_queue: Queue with workers search results
    :return: Merged search results from workers
    """
    result: dict[str, list[str]] = {keyword: [] for keyword in keywords}
    search_done_count: int = 0
    while search_done_count < worker_numbers:
        # Blocking retrieval — without Busy Wait
        file, found_keywords = results_queue.get()
        if file == SearchEngine.sentinel:
            search_done_count += 1
            continue
        for keyword in found_keywords:
            result[keyword].append(file)
    return result