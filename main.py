
import sys

try:
    import curses
except ImportError:
    if sys.platform == "win32":
        import curses
    else:
        raise

from tui.controller import TuiController


def main(stdscr):
    controller = TuiController(stdscr)
    controller.run()


if __name__ == "__main__":
    curses.wrapper(main)
