# -*- coding: utf-8 -*-

"""
HomeWork Task 1
"""

import os
import time
import collections
import logging
from pathlib import Path
from threading import Thread
from queue import Queue

from .data import split_files_evenly
from .file import load_text_file_data
from .boyer_moore import boyer_moore_search


class SearchEngine:

    def __init__(self, idx: int, files: list[Path], keywords: list[str], results_queue: Queue[dict[str, list[Path]]]):
        self.idx = idx

        self.files  = files
        self.keywords = keywords
        self.results_queue = results_queue

        self.logger: logging.Logger = logging.getLogger(__name__)

    def __call__(self, *args, **kwargs) -> None:
        """
        Searches for keywords in a set of files and writes the result to a queue.
        """
        try:
            result: dict[str, list[Path]] = collections.defaultdict(list[Path])
            for file in self.files:
                self.search_keywords_in_file(file, result)
            self.results_queue.put(result)
        except Exception as e:
            self.logger.error(e)

    def search_keywords_in_file(self, file: Path, result: dict[str, list[Path]]) -> None:
        """
        Searches for keywords in a file and writes the result to the specified dictionary.

        :param file: The file in which the search must be performed
        :param result: The dictionary where the result must be recorded
        """
        try:
            self.logger.info(f"Search in the file \"{file.as_posix()}\"")
            text: str = load_text_file_data(file)
            for keyword in self.keywords:
                if boyer_moore_search(text, keyword, find_all=False):
                    result[keyword].append(file)
                    self.logger.info(f"Keyword \"{keyword}\" found in the file \"{file.as_posix()}\"")
        except Exception as e:
            self.logger.error(e)


def multithreading_search(files: list[Path], keywords: list[str]) -> tuple[dict[str, list[Path]], float]:

    logging.basicConfig(format="%(asctime)s %(threadName)s %(levelname)s %(message)s", level=logging.INFO)

    start_time: float = time.perf_counter()

    thread_number: int = os.cpu_count() or 1
    files_for_process = split_files_evenly(files, thread_number)
    threads: list[Thread] = []
    results_queue: Queue[dict[str, list[Path]]] = Queue()

    for i in range(thread_number):
        search_engine = SearchEngine(i, files_for_process[i], keywords, results_queue)
        thread = Thread(target=search_engine, name=f"Search Engine #{i}")
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]

    result: dict[str, list[Path]] = {keyword: [] for keyword in keywords}
    while not results_queue.empty():
        thread_result = results_queue.get()
        for keyword, files in thread_result.items():
            result[keyword].extend(files)

    return result, round(time.perf_counter() - start_time, 6),
