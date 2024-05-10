import tkinter
import tkinter as tk
from tkinter import simpledialog
from typing import Any
import copy


class SelectDialog(simpledialog.Dialog):
    def __init__(self,
                 master: tk.Tk,
                 title=None,
                 select_data: dict[str, Any] = {},
                 extra_infomation: dict[str, str] = {}) -> None:
        self._title = title
        self._parent = master
        self._select_data = select_data
        self.extra_infomation = extra_infomation

        self.result: Any = None
        super().__init__(self._parent, title)

    def body(self, master: tk.Tk):
        tk.Label(master, text=self._title).pack()

    def buttonbox(self):
        box = tk.Frame(self)
        for label, data in self._select_data.items():
            select_frame = tk.Frame(box)
            _data = copy.copy(data)
            tk.Button(select_frame,
                      text=label,
                      command=self.select(data)).pack(side=tk.LEFT, anchor=tk.W)
            if label in self.extra_infomation:
                tk.Label(select_frame,
                         text=self.extra_infomation[label]).pack(side=tk.LEFT, anchor=tk.W)
            select_frame.pack(anchor=tk.W)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def select(self, data: Any):
        _data = copy.copy(data)

        def _select():
            self.result = _data
            self.ok()
        return _select


class CustomDialog(simpledialog.Dialog):
    def __init__(self, master: tk.Tk, title=None) -> None:
        parent = master
        tk.Toplevel.__init__(self, parent, bg="red")

        self.withdraw()
        if parent.winfo_viewable():
            self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        if self.parent is not None:
            self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                      parent.winfo_rooty() + 50))

        self.deiconify()

        self.initial_focus.focus_set()

        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)


if __name__ == "__main__":
    root = tkinter.Tk()

    def display_dialog():
        CustomDialog(root)

    button = tk.Button(root)
    button["text"] = "ダイアログ表示"
    button["command"] = display_dialog
    button.grid(column=0, row=0, padx=10, pady=10)

    root.mainloop()
