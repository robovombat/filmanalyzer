
# [MODIFIED STEP: Step 2c - Rich-Curses Hybrid | 2025-03-31]
# CHANGES:
# - RichHandler w/ colorized log level
# - File and console logger

import logging
from rich.logging import RichHandler
from rich.console import Console
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

FORMAT = "[%(levelname).1s] %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"

console = Console()

logger = logging.getLogger("FilmAnalyzer")
logger.setLevel(logging.DEBUG)
logger.handlers.clear()

rich_handler = RichHandler(console=console, markup=True)
rich_handler.setLevel(logging.INFO)
rich_handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATEFMT))
logger.addHandler(rich_handler)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt=DATEFMT))
logger.addHandler(file_handler)

log = logger
