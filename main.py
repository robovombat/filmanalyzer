# [MODIFIED STEP: Step 2d - Shell Test Trigger (No __init__) | 2025-03-31 17:54]
# CHANGES:
# - Replaced runpy with direct file execution via open/exec
# - Avoided need for tests/__init__.py
# - CLI trigger: python main.py test-shell

import sys
import curses
from log.logger import log
from settings.loader import load_config

# 🎮 Main curses interface
def main(stdscr):
    from tui.controller import TuiController
    config = load_config()
    log.info(f"[SETTINGS] input_mode = {config.get('terminal_input_mode')}")
    controller = TuiController(stdscr, config)
    controller.run()

# 🧪 Simple test file executor (manual, safe fallback)
def run_command_shell_test():
    print("🔧 Running Command Shell Test...\n")
    with open("tests/test_shell.py", "r", encoding="utf-8") as f:
        code = f.read()
        exec(code, {"__name__": "__main__"})

# 🧭 Entry point switcher
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test-shell":
        run_command_shell_test()
    else:
        curses.wrapper(main)
