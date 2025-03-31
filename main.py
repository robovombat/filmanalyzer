
import sys
try:
    import curses
except ImportError:
    if sys.platform == "win32":
        import curses
    else:
        raise

from tui.controller import TuiController
from log.logger import log

def main(stdscr):
    log.info("🔁 App Starting")
    controller = TuiController(stdscr)
    controller.run()
    log.info("✅ App Exited Successfully")

if __name__ == "__main__":
    curses.wrapper(main)
