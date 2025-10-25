# -*- coding: utf-8 -*-

"""
HomeWork Task 2
"""

import os
import time
from multiprocessing import Process, Queue
from pathlib import Path

from .data import split_files_evenly
from .search import SearchEngine, collect_search_result


def multiprocessing_search(files: list[Path], keywords: list[str]) -> tuple[dict[str, list[str]], float]:

    start_time: float = time.perf_counter()

    process_number: int = os.cpu_count() or 1
    files_for_process = split_files_evenly(files, process_number)
    processes: list[Process] = []
    results_queue: "Queue[tuple[str, list[str]]]" = Queue()

    for i in range(process_number):
        search_engine = SearchEngine(i, files_for_process[i], keywords, results_queue)
        process = Process(target=search_engine, name=f"Search Engine #{i}")
        process.start()
        processes.append(process)

    # Collect the search results
    result: dict[str, list[str]] = collect_search_result(keywords, process_number, results_queue)

    # Make sure all workers have finished their execution and shut down
    for process in processes:
        process.join()

    return result, round(time.perf_counter() - start_time, 6),
