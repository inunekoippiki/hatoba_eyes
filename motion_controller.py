import tkinter as tk
import logging
from motion import IrisDirectionMotion
from eyes import Eyes
logger = logging.getLogger()


class MonitonController:
    def __init__(
        self,
        master: tk.Tk,
        eyes: Eyes
    ) -> None:
        self.eyes = eyes
        controll_frame = tk.Frame(master)
        blink_button = tk.Button(controll_frame, text="瞬き", command=self.blink)
        blink_button.pack()

        controll_frame.pack(side=tk.TOP, anchor=tk.N)
        self.eye_direction_motion_right = IrisDirectionMotion()
        self.eye_direction_motion_left = IrisDirectionMotion()

    def update(self, delta_time: float):
        pass

    def draw(self):
        pass

    def blink(self):
        self.eyes.eyelids.blink()

    def direction(self, x: int, y: int):
        self.eye_direction_motion_right.x = x
        self.eye_direction_motion_right.y = y
        self.eye_direction_motion_left.x = x
        self.eye_direction_motion_left.y = y
