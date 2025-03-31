
import os

def read_last_lines(filepath, num_lines=10):
    if not os.path.exists(filepath):
        return ["[LOG] File not found."]
    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()
        return lines[-num_lines:] if lines else ["[LOG] No entries found."]
