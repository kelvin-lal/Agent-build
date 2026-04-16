"""
Kelvin's Agent
"""

import os
import json

SETTINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "agent_settings.json")

DEFAULTS = {
    "submission_interval": 1.0,
    "custom_tags": [],
}


class Settings:
    def load(self):
        if not os.path.isfile(SETTINGS_FILE):
            return dict(DEFAULTS)
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
            merged = dict(DEFAULTS)
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError) as e:
            print(f"[WARN] Could not read settings file, using defaults: {e}")
            return dict(DEFAULTS)

    def save(self, data):
        try:
            os.makedirs(SETTINGS_DIR, exist_ok=True)
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"[ERROR] Failed to save settings: {e}")

    def purge(self):
        try:
            if os.path.isfile(SETTINGS_FILE):
                os.remove(SETTINGS_FILE)
            if os.path.isdir(SETTINGS_DIR) and not os.listdir(SETTINGS_DIR):
                os.rmdir(SETTINGS_DIR)
        except OSError as e:
            print(f"[ERROR] Failed to purge settings: {e}")


settings = Settings()
