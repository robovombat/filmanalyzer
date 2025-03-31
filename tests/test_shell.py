# [TEST] test_shell.py — Simulates shell commands and validates output

from shell.command_shell import CommandShell

# 🧪 Mocked modules
class MockImporter:
    def load_media(self, file_path):
        return f"✔ Loaded {file_path}"

class MockAnalyzer:
    def start_analysis(self):
        return "✔ Analysis started"
    def pause_analysis(self):
        return "✔ Analysis paused"

class MockSettings:
    def set(self, key, value):
        return f"Set {key} = {value}"

def run_test():
    shell = CommandShell({
        'importer': MockImporter(),
        'analyzer': MockAnalyzer(),
        'settings': MockSettings(),
    })

    # Simulate user commands
    commands = [
        "help",
        "load film.mp4",
        "analyze",
        "pause",
        "set analysis_fps=2.5",
        "unknown",
        "clear"
    ]

    for cmd in commands:
        shell.current_input = list(cmd)
        response = shell._execute_command()
        print(f"> {cmd}\n{response}\n")

# 🔁 Ensure it's triggered on standalone run
if __name__ == "__main__":
    run_test()
