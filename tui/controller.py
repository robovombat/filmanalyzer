
import curses

class TuiController:
    """
    Main TUI Controller handles:
    - Key input
    - Tab rendering
    - App lifecycle
    """

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.tabs = ["Terminal", "Log", "Commands", "Statistics", "Tasks", "Settings ⚙"]
        self.active_tab = 0

        # Setup
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
        content_text = f"🧪 You are in the [{self.tabs[self.active_tab]}] tab."
        self.stdscr.addstr(height // 2, max(2, width // 4), content_text)

    def run(self):
        while True:
            self.stdscr.clear()
            self.draw_tabs()
            self.draw_footer()
            self.draw_content()
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key in [curses.KEY_RIGHT, ord('l')]:
                self.active_tab = (self.active_tab + 1) % len(self.tabs)
            elif key in [curses.KEY_LEFT, ord('h')]:
                self.active_tab = (self.active_tab - 1) % len(self.tabs)
            elif key in [ord('q'), ord('Q')]:
                break
