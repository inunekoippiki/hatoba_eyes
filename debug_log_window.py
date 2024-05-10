import tkinter as tk
from tkinter import scrolledtext

TEXT_COLORS = {
    "MESSAGE": "black",
    "INPUT": "blue",
    "OUTPUT": "green",

    "DEBUG": "green",
    "INFO": "black",
    "WARNING": "yellow",
    "ERROR": "red"
}


class SimpleCheck(tk.Checkbutton):
    def __init__(self, parent, *args, **kw):
        self.flag = kw.pop("flag")
        self.var = tk.BooleanVar()
        if self.flag:
            self.var.set(True)
        self.txt = kw["text"]
        tk.Checkbutton.__init__(self, parent, *args, **kw, variable=self.var)

    def get(self):
        return self.var.get()


class DebugLogFrame(tk.Frame):
    def __init__(self, master: tk.Tk):
        tk.Frame.__init__(self, master)
        master.title("debug_monitor")

        select_frame = tk.LabelFrame(
            master, text="Log text disable", relief="groove")

        self.ckboxs = []
        for key in TEXT_COLORS:
            cb = SimpleCheck(select_frame, text=key,
                             command=self.callback, flag=False)
            self.ckboxs.append(cb)
            cb.pack(side="left")
        select_frame.pack(side="top", fill="x")

        self.txt = scrolledtext.ScrolledText(master)
        self.txt.pack(fill=tk.BOTH, expand=1)
        for key in TEXT_COLORS:
            self.txt.tag_config(key, foreground=TEXT_COLORS[key])

    def callback(self):
        count = 0
        for key in TEXT_COLORS:
            if (self.ckboxs[count].get()):
                self.hide(key)
            else:
                self.view(key)
            count += 1

    def print(self, str, state="MESSAGE"):
        self.txt.insert(tk.END, str+"\n", state)
        self.txt.see(tk.END)

    def hide(self, tag):
        self.txt.tag_config(tag, elide=True)

    def view(self, tag):
        self.txt.tag_config(tag, elide=False)

    def write(self, str, state="MESSAGE"):
        self.txt.insert(tk.END, str+"\n", state)
        self.txt.see(tk.END)

    def flush(self):
        pass
