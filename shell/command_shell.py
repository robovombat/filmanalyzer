# [ADDED STEP: Step 2d - Modular Command Shell Integration | 2025-03-31]
# LOCATION: shell/command_shell.py
# CHANGES:
# - Modular terminal shell command processor
# - Integrated module calling
# - History, settings handling, help system

import curses
from functools import partial
from typing import Dict, List, Callable, Optional

class CommandShell:
    """🔧 Terminal command interface with history and module integration"""

    def __init__(self, modules: Dict[str, object]):
        # █ History
        self.history: List[str] = []
        self.history_index: int = -1
        self.current_input: List[str] = []

        # █ Injected modules
        self.modules = modules

        # █ Command definitions
        self.command_registry = self._build_command_registry()

        # █ Autocomplete (future)
        self.autocomplete_options: List[str] = []
        self.autocomplete_index: int = 0

    def _build_command_registry(self) -> Dict[str, Callable]:
        """📚 Define available commands and their handlers"""
        return {
            'load': partial(self._execute_module, 'importer', 'load_media'),
            'save': partial(self._execute_module, 'exporter', 'save_results'),
            'analyze': partial(self._execute_module, 'analyzer', 'start_analysis'),
            'pause': partial(self._execute_module, 'analyzer', 'pause_analysis'),
            'set': self._handle_settings,
            'help': self._show_help,
            'clear': self._clear_screen,
            'exit': self._exit_program,
        }

    def process_input(self, win: curses.window, key: int) -> Optional[str]:
        """⌨️ Handle terminal input events"""
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
        if not self.history:
            return
        self.history_index = max(min(self.history_index + direction, -1), -len(self.history))
        self.current_input = list(self.history[self.history_index])

    def _execute_command(self) -> str:
        """🧠 Execute a parsed terminal command"""
        cmd_str = ''.join(self.current_input).strip()
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
        """🔌 Call injected module's method"""
        module = self.modules.get(module_name)
        if not module:
            return f"Module '{module_name}' not available"
        method = getattr(module, method_name, None)
        if not method:
            return f"'{module_name}' has no method '{method_name}'"
        return method(*args)

    def _handle_settings(self, *args):
        """⚙️ Change runtime settings"""
        if not args or '=' not in args[0]:
            return "Usage: set key=value"
        key, value = args[0].split("=", 1)
        settings = self.modules.get("settings")
        if not settings:
            return "Settings module not available"
        return settings.set(key.strip(), value.strip())

    def _show_help(self):
        return "Commands: load <file>, save, analyze, pause, set k=v, help, clear, exit"

    def _clear_screen(self):
        return "[OK] Screen cleared."

    def _exit_program(self):
        raise SystemExit("User exited.")
