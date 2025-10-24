# -*- coding: utf-8 -*-

__title__ = 'Home Work Tasks'
__author__ = 'Roman'

from .task_01 import multithreading_search
from .task_02 import multiprocessing_search
from .data import get_files, get_keywords, split_files_evenly
from .generate_test_data import test_data_generate

__all__ = [
    'multithreading_search',
    'multiprocessing_search',
    'get_files',
    'get_keywords',
    'split_files_evenly',
    'test_data_generate',
]
