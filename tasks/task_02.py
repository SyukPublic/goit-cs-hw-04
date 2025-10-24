# -*- coding: utf-8 -*-

"""
HomeWork Task 2
"""

import time
from pathlib import Path


def multiprocessing_search(files: list[Path], keywords: list[str]) -> tuple[dict[str, list[Path]], float]:
    start_time: float = time.perf_counter()

    return {}, round(time.perf_counter() - start_time, 6),
