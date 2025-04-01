# [STEP: Step 3.3 - Extract Progress Callback | INITIAL: 2025-03-31 19:04 | MODIFIED: 2025-04-01 18:42]
# LOCATION: shell/command_shell.py
# CHANGES:
# - Added real-time progress bar using terminal_output
# - Added -fps parsing to extract command
# - Uses lambda callback for extract_frames()
# - Retains full compatibility with run_text_command()

import curses
from functools import partial
from typing import Dict, List, Callable, Optional

class CommandShell:
    """🔧 Terminal command interface with history and module integration"""

    def __init__(self, modules: Dict[str, object]):
        # 🧠 CLI state
        self.history: List[str] = []
        self.history_index: int = -1
        self.current_input: List[str] = []

        # 🔌 External module references
        self.modules = modules

        # 📦 Terminal display (shared with TUI controller)
        self.terminal_output: List[str] = []

        # 📚 Command routing
        self.command_registry = self._build_command_registry()

        # 💡 Future feature: autocomplete
        self.autocomplete_options: List[str] = []
        self.autocomplete_index: int = 0

    def _build_command_registry(self) -> Dict[str, Callable]:
        return {
            'load': partial(self._execute_module, 'importer', 'load_media'),
            'save': partial(self._execute_module, 'exporter', 'save_results'),
            'analyze': partial(self._execute_module, 'analyzer', 'start_analysis'),
            'pause': partial(self._execute_module, 'analyzer', 'pause_analysis'),
            'extract': self._run_extract_with_progress,
            'set': self._handle_settings,
            'help': self._show_help,
            'clear': self._clear_screen,
            'exit': self._exit_program,
        }

    def _run_extract_with_progress(self, *args) -> str:
        """🎞️ Extract frames using importer.extract_frames with progress callback"""
        fps = 1.0
        for arg in args:
            if arg.startswith("-fps="):
                try:
                    fps = float(arg.split("=")[-1])
                except ValueError:
                    return "[warn] Invalid FPS value"

        importer = self.modules.get("importer")
        if not importer:
            return "[error] Importer module not found"

        # ⏳ Progress callback appending progress bar to output
        def push_progress(percent, eta):
            bar = f"[info] Extract progress: [{'█' * (percent // 10)}{'░' * (10 - percent // 10)}] {percent}% (ETA: {eta}s)"
            self.terminal_output.append(bar)

        return importer.extract_frames(fps=fps, on_progress=push_progress)

    def process_input(self, win: curses.window, key: int) -> Optional[str]:
        """🧠 Capture interactive input via curses"""
        if key == curses.KEY_UP:
            self._navigate_history(-1)
        elif key == curses.KEY_DOWN:
            self._navigate_history(1)
        elif key in (curses.KEY_ENTER, 10, 13):
            return self._execute_command()
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if self.current_input:
                self.current_input.pop()
        elif 32 <= key <= 126:
            self.current_input.append(chr(key))
        return ""

    def _navigate_history(self, direction: int):
        """📜 Scroll through previous commands"""
        if not self.history:
            return
        self.history_index = max(min(self.history_index + direction, -1), -len(self.history))
        self.current_input = list(self.history[self.history_index])

    def _execute_command(self) -> str:
        """🎮 Parse and execute full user command"""
        cmd_str = ''.join(self.current_input).strip()
        if cmd_str.startswith(">"):
            cmd_str = cmd_str[1:].lstrip()
        if not cmd_str:
            return ""
        self.history.append(cmd_str)
        self.history_index = -1
        self.current_input = []

        parts = cmd_str.split()
        base_cmd = parts[0].lower()
        args = parts[1:]

        if base_cmd not in self.command_registry:
            return f"[?] Unknown command: {base_cmd}"

        try:
            result = self.command_registry[base_cmd](*args)
            return f"[OK] {result}" if result else "[OK] Done"
        except Exception as e:
            return f"[error] Execution Error: {str(e)}"

    def _execute_module(self, module_name: str, method_name: str, *args):
        """🔌 Dynamic module method calling"""
        module = self.modules.get(module_name)
        if not module:
            return f"[error] Module '{module_name}' not available"
        method = getattr(module, method_name, None)
        if not method:
            return f"[error] No method '{method_name}' in module '{module_name}'"
        return method(*args)

    def _handle_settings(self, *args):
        """⚙️ Set key=value runtime parameters"""
        if not args or '=' not in args[0]:
            return "Usage: set key=value"
        key, value = args[0].split("=", 1)
        settings = self.modules.get("settings")
        if not settings:
            return "Settings module not available"
        return settings.set(key.strip(), value.strip())

    def _show_help(self):
        return "Commands: load <file>, extract -fps=, save, analyze, pause, set k=v, help, clear, exit"

    def _clear_screen(self):
        self.terminal_output.clear()
        return "[OK] Screen cleared."

    def _exit_program(self):
        raise SystemExit("User exited.")

    def run_text_command(self, command: str) -> str:
        """🧪 Public function for testing or TUI to inject commands"""
        self.current_input = list(command.strip())
        return self._execute_command()
