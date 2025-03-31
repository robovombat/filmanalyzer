# [ADDED STEP: ConfigManager for Shell Integration | 2025-03-31 19:35]
# CHANGES:
# - Adds ConfigManager class with `set()` support for CLI

class ConfigManager:
    """⚙️ Runtime configuration manager for TUI + shell"""

    def __init__(self):
        self.config = {
            "analysis_fps": 1.0,
            "export_format": "json",
            "log_level": "info"
        }

    def set(self, key: str, value: str) -> str:
        if key not in self.config:
            raise KeyError(f"Invalid setting: {key}")
        expected_type = type(self.config[key])
        try:
            self.config[key] = expected_type(value)
        except Exception:
            raise ValueError(f"Cannot cast {value} to {expected_type.__name__}")
        return f"Set {key} to {value}"


