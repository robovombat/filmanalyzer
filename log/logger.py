
import logging
from rich.console import Console
from rich.logging import RichHandler
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
os.makedirs(LOG_DIR, exist_ok=True)

FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"

console = Console()

logger = logging.getLogger("FilmAnalyzer")
logger.setLevel(logging.DEBUG)

logger.handlers.clear()

console_handler = RichHandler(console=console, markup=True)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATEFMT))
logger.addHandler(console_handler)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(FORMAT, datefmt=DATEFMT))
logger.addHandler(file_handler)

log = logger
