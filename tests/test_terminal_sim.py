
# [MODIFIED STEP: Step 2c - Rich-Curses Hybrid | 2025-03-31]
# CHANGES:
# - Simulate terminal output with color-coded rich log

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from log.logger import log

def test_terminal_rich_output():
    log.info("[green][OK][/green] Test passed")
    log.info("[red][error][/red] Something went wrong")
    log.info("[cyan][info][/cyan] Info is flowing")
    log.info("[magenta][?][/magenta] What is this?")
    print("✅ Log messages emitted to terminal and log file")

if __name__ == "__main__":
    test_terminal_rich_output()
