# [MODIFIED STEP: Step 2e - Hooked Shell into Controller | 2025-03-31 19:24]
# CHANGES:
# - Injected CommandShell into controller
# - Linked real importer, analyzer, settings modules
# - Replaced manual command parser with shell.run_text_command()

import curses
import os

# ✅ Modular shell interface
from shell.command_shell import CommandShell

# ✅ Utility/log modules
from log.viewer import read_last_lines
from log.logger import log
from settings.loader import save_config

# ✅ CommandShell backends
from modules.importer import MediaImporter
from modules.analyzer import VideoAnalyzer
from modules.settings import ConfigManager


class TuiController:
    def __init__(self, stdscr, config):
        # █ UI + State
        self.stdscr = stdscr
        self.tabs = ["Terminal", "Log", "Commands", "Statistics", "Tasks", "Settings ⚙"]
        self.active_tab = 0
        self.log_path = os.path.join("logs", "app.log")
        self.config = config

        # █ Mode Setup
        self.input_mode = config.get("terminal_input_mode", "hybrid")
        self.is_in_insert_mode = self.input_mode == "hybrid"

        self.input_buffer = ""
        self.terminal_output = []
        self.command_history = []
        self.history_index = -1
        self.scroll_offset = 0

        # █ Inject real command modules
        self.modules = {
            'importer': MediaImporter(),
            'analyzer': VideoAnalyzer(),
            'settings': ConfigManager(),
        }
        self.command_shell = CommandShell(self.modules)

        # █ Curses init
        curses.curs_set(0)
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)

    def draw_tabs(self):
        height, width = self.stdscr.getmaxyx()
        tab_str = ""
        for i, tab in enumerate(self.tabs):
            if i == self.active_tab:
                tab_str += f"[{tab}]│"
            else:
                tab_str += f" {tab} │"
        self.stdscr.addstr(0, 0, tab_str[:width - 1], curses.A_BOLD)

    def draw_footer(self):
        height, width = self.stdscr.getmaxyx()
        footer_text = "←/→ Switch Tabs   |   [Q] Quit"
        self.stdscr.addstr(height - 1, 0, footer_text[:width - 1], curses.A_DIM)

    def draw_content(self):
        height, width = self.stdscr.getmaxyx()
        current_tab = self.tabs[self.active_tab]

        if current_tab == "Log":
            log_lines = read_last_lines(self.log_path, num_lines=height - 4)
            for i, line in enumerate(log_lines):
                if i + 2 < height - 1:
                    self.stdscr.addstr(i + 2, 2, line.strip()[:width - 4])

        elif current_tab == "Terminal":
            max_output_lines = height - 5
            visible_output = self.terminal_output[-max_output_lines:]
            for i, line in enumerate(visible_output):
                self.draw_colored_line(i + 2, 2, line[:width - 4])
            prompt = f"> {self.input_buffer}"
            self.stdscr.addstr(height - 3, 2, prompt[:width - 4], curses.A_UNDERLINE)

        else:
            content_text = f"You are in the [{current_tab}] tab."
            self.stdscr.addstr(height // 2, max(2, width // 4), content_text)

    def draw_colored_line(self, y, x, line):
        # 🔷 Add rich style later – currently monocolor
        self.stdscr.addstr(y, x, line)

    def handle_terminal_input(self, key):
        if self.input_mode == "vim":
            if self.is_in_insert_mode:
                self.handle_input_key(key)
            else:
                if key == ord('i'):
                    self.is_in_insert_mode = True
                    self.terminal_output.append("[info] Insert mode activated")
                elif key == 27:  # ESC
                    self.terminal_output.append("[info] Already in navigation mode")
        else:
            self.handle_input_key(key)

    def handle_input_key(self, key):
        if key in (curses.KEY_ENTER, 10, 13):
            command = self.input_buffer.strip()
            if command:
                self.command_history.append(command)
                self.history_index = -1
                self.execute_command(command)
            self.input_buffer = ""

        elif key in (curses.KEY_BACKSPACE, 127, 8):
            self.input_buffer = self.input_buffer[:-1]

        elif key == curses.KEY_UP:
            if self.command_history:
                self.history_index = max(self.history_index - 1, -len(self.command_history))
                self.input_buffer = self.command_history[self.history_index]

        elif key == curses.KEY_DOWN:
            if self.history_index < -1:
                self.history_index += 1
                self.input_buffer = self.command_history[self.history_index]
            else:
                self.input_buffer = ""

        elif 32 <= key <= 126:
            self.input_buffer += chr(key)

        elif key == 27 and self.input_mode == "vim":
            self.is_in_insert_mode = False
            self.terminal_output.append("[info] Switched to navigation mode")

    def execute_command(self, command: str):
        """🧪 Delegate to CommandShell"""
        result = self.command_shell.run_text_command(command)
        if result:
            self.terminal_output.append(result)
            log.info(f"[TERMINAL] response: {result}")

    def run(self):
        while True:
            self.stdscr.clear()
            self.draw_tabs()
            self.draw_footer()
            self.draw_content()
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if self.tabs[self.active_tab] == "Terminal":
                if self.input_mode == "hybrid" and self.input_buffer == "":
                    if key == curses.KEY_LEFT:
                        self.active_tab = (self.active_tab - 1) % len(self.tabs)
                        continue
                    elif key == curses.KEY_RIGHT:
                        self.active_tab = (self.active_tab + 1) % len(self.tabs)
                        continue
                self.handle_terminal_input(key)

            elif key == curses.KEY_RIGHT:
                self.active_tab = (self.active_tab + 1) % len(self.tabs)
            elif key == curses.KEY_LEFT:
                self.active_tab = (self.active_tab - 1) % len(self.tabs)
            elif key in [ord('q'), ord('Q')]:
                break
