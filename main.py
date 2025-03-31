
# [MODIFIED STEP: Step 2c - Rich-Curses Hybrid | 2025-03-31]
# CHANGES:
# - App boot with config + TUI startup
# - Logs config mode
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
from settings.loader import load_config

def main(stdscr):
    config = load_config()
    log.info("[SETTINGS] Loaded from config/config.yaml")
    log.info(f"[SETTINGS] input_mode = {config.get('terminal_input_mode')}")
    controller = TuiController(stdscr, config)
    controller.run()
    log.info("✅ App Exited Successfully")

if __name__ == "__main__":
    curses.wrapper(main)
