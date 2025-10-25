# -*- coding: utf-8 -*-

"""
HomeWork Task 1
"""

import logging
import os
import time
from queue import Queue
from pathlib import Path
from threading import Thread

from .data import split_files_evenly
from .logger import logger_init
from .search import SearchEngine, collect_search_result


def multithreading_search(files: list[Path], keywords: list[str]) -> tuple[dict[str, list[str]], float]:

    logger: logging.Logger = logger_init(name=__name__, thread=True)

    start_time: float = time.perf_counter()

    thread_number: int = os.cpu_count() or 1
    files_for_process = split_files_evenly(files, thread_number)
    threads: list[Thread] = []
    results_queue: "Queue[tuple[str, list[str]]]" = Queue()

    for i in range(thread_number):
        search_engine = SearchEngine(i, files_for_process[i], keywords, results_queue, thread=True, logger=logger)
        thread = Thread(target=search_engine, name=f"Search Engine #{i}")
        thread.start()
        threads.append(thread)

    # Collect the search results
    result: dict[str, list[str]] = collect_search_result(keywords, thread_number, results_queue)

    # Make sure all workers have finished their execution and shut down
    for thread in threads:
        thread.join()

    return result, round(time.perf_counter() - start_time, 6),
