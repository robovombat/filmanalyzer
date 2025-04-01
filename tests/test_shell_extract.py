# [TEST] test_shell_extract.py
# PURPOSE: Validate shell command 'extract' triggers importer

from shell.command_shell import CommandShell
from modules.importer import MediaImporter

def run_test():
    importer = MediaImporter()
    importer.load_media("assets/test.mp4")
    shell = CommandShell({'importer': importer})
    result = shell.run_text_command("extract -fps=2.0")
    print("[TEST] Shell Extract Output:", result)
