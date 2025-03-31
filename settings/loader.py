
# [MODIFIED STEP: Step 2c - Rich-Curses Hybrid | 2025-03-31]
# CHANGES:
# - Load/save YAML config from disk

import os
import yaml

CONFIG_PATH = os.path.join("config", "config.yaml")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {"terminal_input_mode": "hybrid"}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_config(new_data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(new_data, f)
