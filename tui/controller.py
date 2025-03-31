# [MODIFIED STEP: Step 2b.4 - Input Mode Setting | 2025-03-30]
# CHANGES:
# - Added terminal_input_mode setting logic
# - Arrow key behavior adapts based on input
# - Added `:set input_mode=` terminal command
# - Color-coded messages using curses.init_pair

import curses
import os
from log.viewer import read_last_lines
from log.logger import log
from settings.loader import save_config

class TuiController:
    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.tabs = ["Terminal", "Log", "Commands", "Statistics", "Tasks", "Settings ⚙"]
        self.active_tab = 0
        self.log_path = os.path.join("logs", "app.log")
        self.config = config

        self.input_mode = config.get("terminal_input_mode", "hybrid")  # "vim" or "hybrid"
        self.is_in_insert_mode = True if self.input_mode == "hybrid" else False

        self.input_buffer = ""
        self.terminal_output = []
        self.command_history = []
        self.history_index = -1
        self.scroll_offset = 0

        curses.curs_set(0)
        self.stdscr.nodelay(False)
        self.stdscr.keypad(True)
        self.init_colors()

def init_colors(self):
    if not curses.has_colors():
        from log.logger import log
        log.warning("[WARN] Terminal does not support color.")
        return

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_GREEN, -1)   # OK
    curses.init_pair(2, curses.COLOR_CYAN, -1)    # Info
    curses.init_pair(3, curses.COLOR_MAGENTA, -1) # ?
    curses.init_pair(4, curses.COLOR_RED, -1)     # Error
    curses.init_pair(5, curses.COLOR_YELLOW, -1)  # Warn
    
    
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
        if line.startswith("[OK]"):
            self.stdscr.addstr(y, x, "[OK]", curses.color_pair(1))
            self.stdscr.addstr(y, x + 4, line[4:])
        elif line.startswith("[info]"):
            self.stdscr.addstr(y, x, "[info]", curses.color_pair(2))
            self.stdscr.addstr(y, x + 6, line[6:])
        elif line.startswith("[?]"):
            self.stdscr.addstr(y, x, "[?]", curses.color_pair(3))
            self.stdscr.addstr(y, x + 3, line[3:])
        elif line.startswith("[warn]"):
            self.stdscr.addstr(y, x, "[warn]", curses.color_pair(5))
            self.stdscr.addstr(y, x + 6, line[6:])
        elif line.startswith("[error]"):
            self.stdscr.addstr(y, x, "[error]", curses.color_pair(4))
            self.stdscr.addstr(y, x + 7, line[7:])
        else:
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
            log.info(f"[TERMINAL] input: {command}")
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

    def execute_command(self, command):
        if command == "help":
            response = "[OK] Commands: help, echo <text>, clear, exit, :set input_mode=..."
        elif command.startswith("echo "):
            response = command[5:].strip()
        elif command == "clear":
            self.terminal_output = []
            response = "[OK] Screen cleared."
        elif command == "exit":
            response = "[info] Exiting terminal shell (not app)."
        elif command.startswith(":set input_mode="):
            mode = command.split("=")[-1].strip()
            if mode in ("vim", "hybrid"):
                self.input_mode = mode
                self.is_in_insert_mode = (mode == "hybrid")
                self.config["terminal_input_mode"] = mode
                save_config(self.config)
                log.info(f"[SETTINGS] Changed input_mode to {mode}")
                response = f"[OK] input_mode set to {mode}"
            else:
                response = "[warn] Invalid mode. Use 'vim' or 'hybrid'."
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
                # Hybrid: allow ←/→ if input is empty
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
