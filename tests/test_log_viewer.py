
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from log.viewer import read_last_lines

def test_log_reading():
    path = "logs/app.log"
    if not os.path.exists(path):
        print("[WARN] Log file doesn't exist.")
        return
    lines = read_last_lines(path, 5)
    print("Last 5 log lines:")
    for line in lines:
        print("  " + line.strip())

if __name__ == "__main__":
    test_log_reading()
