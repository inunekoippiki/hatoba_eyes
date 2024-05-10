import tkinter as tk
from typing import Any


class DebugMonitorWindow():
    def __init__(self, root: tk.Tk) -> None:
        self.labels: dict[str, tk.Label] = {}
        self.window = tk.Toplevel(root)
        self.window.title("debug_monitor")
        pass

    def print(self, label: str, value: Any):
        text = f"{label} : {value}"
        if label not in self.labels:
            w = tk.Label(self.window, text=text)
            w.pack(anchor=tk.W)
            self.labels[label] = w
        else:
            self.labels[label]["text"] = text
