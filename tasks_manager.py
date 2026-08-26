from pathlib import Path
import sys

class TaskManager:
    def __init__(self):
        if sys.platform == "darwin" or sys.platform == "linux":
            self.path = Path.home() / ".config" / "Dashboard" / "tasks.md"
        elif sys.platform == "win32":
            self.path = Path.home() / "AppData" / "Roaming" / "Dashboard" / "tasks.md"
        else:
            raise RuntimeError(f"Platform not supported: {sys.platform}")

    def read_tasks(self):
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("# Tasks\n\n")

        return self.path.read_text(encoding="utf-8")

    def write_tasks(self, text):
        self.path.write_text(text, encoding="utf-8")