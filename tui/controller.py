# FILE: tui/controller.py

import curses
from log.viewer import read_last_lines
from log.logger import log
import os


class TuiController:
    """
    Main TUI controller class.
    Handles rendering views, switching tabs, logging, and user input.
    """

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.tabs = ["Terminal", "Log", "Commands", "Statistics", "Tasks", "Settings ⚙"]
        self.active_tab = 0
        self.log_path = os.path.join("logs", "app.log")

        # Terminal shell input/output buffers
        self.input_buffer = ""
        self.terminal_output = []  # stores printed lines from commands

        curses.curs_set(0)               # Hide cursor
        self.stdscr.nodelay(False)       # Blocking mode
        self.stdscr.keypad(True)         # Enable arrow keys, etc.

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
            # Read last N lines from the log file
            log_lines = read_last_lines(self.log_path, num_lines=height - 4)
            for i, line in enumerate(log_lines):
                if i + 2 < height - 1:
                    self.stdscr.addstr(i + 2, 2, line.strip()[:width - 4])

        elif current_tab == "Terminal":
            # Render terminal shell history
            max_output_lines = height - 5
            visible_output = self.terminal_output[-max_output_lines:]
            for i, line in enumerate(visible_output):
                self.stdscr.addstr(i + 2, 2, line[:width - 4])

            # Draw prompt
            prompt = f"> {self.input_buffer}"
            self.stdscr.addstr(height - 3, 2, prompt[:width - 4], curses.A_UNDERLINE)

        else:
            # Placeholder content
            content_text = f"You are in the [{current_tab}] tab."
            self.stdscr.addstr(height // 2, max(2, width // 4), content_text)

    def handle_terminal_input(self, key):
        """
        Process typing and command handling in the terminal tab
        """
        if key in (curses.KEY_ENTER, 10, 13):
            command = self.input_buffer.strip()
            log.info(f"[TERMINAL] input: {command}")
            self.execute_command(command)
            self.input_buffer = ""
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            self.input_buffer = self.input_buffer[:-1]
        elif 32 <= key <= 126:  # Printable ASCII
            self.input_buffer += chr(key)

    def execute_command(self, command):
        """
        Handle recognized commands and append result to output
        """
        if command == "help":
            response = "[OK] Commands: help, echo <text>, clear, exit"
        elif command.startswith("echo "):
            response = command[5:].strip()
        elif command == "clear":
            self.terminal_output = []
            response = "[OK] Screen cleared."
        elif command == "exit":
            response = "[info] Exiting terminal shell (not app)."
        elif command == "":
            response = ""
        else:
            response = f"[?] Unknown command: {command}"

        if response:
            self.terminal_output.append(f"> {command}")
            self.terminal_output.append(response)
            log.info(f"[TERMINAL] response: {response}")

    def run(self):
        while True:
            self.stdscr.clear()
            self.draw_tabs()
            self.draw_footer()
            self.draw_content()
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if self.tabs[self.active_tab] == "Terminal":
                self.handle_terminal_input(key)

            elif key in [curses.KEY_RIGHT, ord('l')]:
                self.active_tab = (self.active_tab + 1) % len(self.tabs)
            elif key in [curses.KEY_LEFT, ord('h')]:
                self.active_tab = (self.active_tab - 1) % len(self.tabs)
            elif key in [ord('q'), ord('Q')]:
                break
