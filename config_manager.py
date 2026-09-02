import sys, json
from pathlib import Path


class ConfigManager:
    def __init__(self):
        if sys.platform == "darwin" or sys.platform == "linux":
            self.path = Path.home() / ".config" / "Dashboard" / "config.json"
        elif sys.platform == "win32":
            self.path = Path.home() / "AppData" / "Roaming" / "Dashboard" / "config.json"
        else:
            raise RuntimeError(f"Platform not supported: {sys.platform}")

        self.path.parent.mkdir(parents=True, exist_ok=True)

    def read_config(self):
        if self.path.exists():
            with open(self.path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            self.init_config()
            with open(self.path, mode="r", encoding="utf-8") as f:
                data = json.load(f)

        return data

    def write_config(self, data: dict):

        with open(self.path, mode="w", encoding="utf-8") as f:
            json.dump(data, f)

    def init_config(self, data = None):
        if not data: # When init config made, remove
            data = {
                "google": False,
                "url": "",
                "user": "",
                "password": "",
                "city": ""
            }

        with open(self.path, mode="w", encoding="utf-8") as f:
            json.dump(data, f)