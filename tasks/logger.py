# -*- coding: utf-8 -*-"

"""
Logger for the tasks
"""

import logging
from typing import Optional


def logger_init(name: Optional[str] = None, thread: bool = False) -> logging.Logger:
    """
    Initialization of the console logger.

    :return: logger instance
    """
    root_logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(threadName)s %(levelname)s %(message)s"
            if thread else
            "%(asctime)s %(processName)s %(levelname)s %(message)s"
        )
    )
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)
    return logging.getLogger(name or __name__)


