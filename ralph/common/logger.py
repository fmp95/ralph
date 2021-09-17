"""
Configure logging system.

This module will configure logging system and make a function to generate a logger
that can be imported by other modules. It will also check if logs folder exists and,
if not, will create one, so it can store log files.
"""

from datetime import datetime
from os import path, mkdir
import logging
import sys

# Check if logs folder exists.
if not path.exists("logs"):
    mkdir("logs")

# Gets current datetime.
now = datetime.now()

# Set filename with current date.
filename = f"{now.year}{now.month}{now.day}.log"

# Create log stream to file.
file_handler = logging.FileHandler(filename="logs/" + filename)

# Create log strem to stdout.
stdout_handler = logging.StreamHandler(sys.stdout)

# Generate configuration of logging.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] %(name)s -> %(message)s",
    handlers=[file_handler, stdout_handler],
)


def get_logger(name: str) -> object:

    """
    Generates a logger with name of file where is writing the log.

    Args:
        name (str): Module name.
    """

    return logging.getLogger(name)
