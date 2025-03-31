
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from log.logger import log

def test_logging_system():
    log.info("🧪 TEST: This is an INFO message")
    log.debug("🧪 TEST: This is a DEBUG message (file only)")
    log.warning("🧪 TEST: This is a WARNING")
    log.error("🧪 TEST: This is an ERROR")

if __name__ == "__main__":
    test_logging_system()
    print("\n✅ Log test complete. Check logs/app.log")
