import logging
import debug_log_window
import tkinter as tk

class GUILogHandler(logging.Handler):
    def __init__(self, master:tk.Tk, level=logging.NOTSET):
      logging.Handler.__init__(self, level=level)
      self._window = tk.Toplevel(master)
      self._frame = debug_log_window.DebugLogFrame(self._window)

    def emit(self, record):
      if len(record.msg) > 0:
        msg = self.format(record)
      else:
        msg = ""
      try:
        self._frame.print(msg,record.levelname)
      except Exception:
        self.handleError(record)

