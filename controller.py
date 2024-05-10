
import tkinter as tk
from enum import Enum, auto
from eyes import Eyes, Eye
import logging
import container
import json
import os
import tkinter.filedialog
import pygame
from event import EventAdjustment

logger = logging.getLogger(__name__)


class ControllType(Enum):
    NOTHING = auto()
    RIGHT_ORIGIN = auto()
    RIGHT_SCALE = auto()
    RIGHT_ANGLE = auto()
    LEFT_ORIGIN = auto()
    LEFT_SCALE = auto()
    LEFT_ANGLE = auto()


class RL(Enum):
    RIGHT = auto()
    LEFT = auto()


class Controller():
    def __init__(self, master: tk.Tk, canvas: tk.Canvas, eyes: Eyes) -> None:
        self.eyes = eyes

        self.canvas = canvas

        self.controll_state = tk.IntVar()

        controll_frame = tk.Frame(master)

        right_frame = tk.Frame(controll_frame)
        read_right = tk.Button(
            right_frame, text="右目画像選択", command=lambda: self.select_image(RL.RIGHT))
        read_right.pack()

        self._create_eye_radio(right_frame, RL.RIGHT)
        right_frame.pack(side=tk.RIGHT, anchor=tk.W)

        left_frame = tk.Frame(controll_frame)
        read_left = tk.Button(
            left_frame, text="左目画像選択", command=lambda: self.select_image(RL.LEFT))
        read_left.pack()

        self._create_eye_radio(left_frame, RL.LEFT)
        left_frame.pack(side=tk.LEFT, anchor=tk.W)

        controll_frame.pack(side=tk.TOP, anchor=tk.N)

        self.action = Action()

        for frame in [right_frame, left_frame]:
            frame.bind_all("<KeyPress>", self.press)

    def _create_eye_radio(self, frame: tk.Frame, rl: RL):
        if rl == RL.RIGHT:
            text, origin, scale, angle = "右目", ControllType.RIGHT_ORIGIN, ControllType.RIGHT_SCALE, ControllType.RIGHT_ANGLE
        else:
            text, origin, scale, angle = "左目", ControllType.LEFT_ORIGIN, ControllType.LEFT_SCALE, ControllType.LEFT_ANGLE

        tk.Radiobutton(
            frame,
            value=origin,
            variable=self.controll_state,
            text=f"{text}中心位置",
            command=lambda: self._on_radio(origin)).pack(anchor=tk.W)
        tk.Radiobutton(
            frame,
            value=scale,
            variable=self.controll_state,
            text=f"{text}拡大縮小",
            command=lambda: self._on_radio(scale)).pack(anchor=tk.W)
        tk.Radiobutton(
            frame,
            value=angle,
            variable=self.controll_state,
            text=f"{text}角度",
            command=lambda: self._on_radio(angle)).pack(anchor=tk.W)

    def _on_radio(self, controll_type: ControllType):
        logger.info(str(controll_type))
        logger.info(str(self.controll_state))

        match controll_type:
            case ControllType.RIGHT_ORIGIN:
                self.action = ActionOrigin(self.eyes.right)
            case ControllType.RIGHT_SCALE:
                self.action = ActionScale(self.eyes.right)
            case ControllType.RIGHT_ANGLE:
                self.action = ActionAngle(self.eyes.right)
            case ControllType.LEFT_ORIGIN:
                self.action = ActionOrigin(self.eyes.left)
            case ControllType.LEFT_SCALE:
                self.action = ActionScale(self.eyes.left)
            case ControllType.LEFT_ANGLE:
                self.action = ActionAngle(self.eyes.left)

    def press(self, event: tk.Event):
        self.action.action(event)
        container.debug_monitor_window.print("eyes", json.dumps(self.eyes.dump(),
                                                                default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def select_image(self, rl: RL):
        iris = self.eyes.irises.right if rl == RL.RIGHT else self.eyes.irises.left
        filetypes = [("", ".png")]
        initialdir = os.path.abspath(os.path.dirname(__file__))
        file_path = tkinter.filedialog.askopenfilename(
            filetypes=filetypes, initialdir=initialdir)
        iris.read_image(file_path)
        logger.info("Select image. rl=%s, file path%s", rl, file_path)


class Action():
    def action(event: tk.Tk):
        pass


class ActionOrigin(Action):
    def __init__(self, eye: Eye) -> None:
        self.eye = eye
        self.move_amount = 1

        super().__init__()

    def action(self, event: tk.Tk):
        event_adjustment = self.event(event)
        self.eye.origin_x += event_adjustment.change_x
        self.eye.origin_y += event_adjustment.change_y

    def event(self, event: tk.Tk) -> EventAdjustment.Param:
        v = pygame.Vector2()
        if event.keysym == "Right":
            v.x += self.move_amount
        elif event.keysym == "Left":
            v.x -= self.move_amount
        elif event.keysym == "Up":
            v.y -= self.move_amount
        elif event.keysym == "Down":
            v.y += self.move_amount

        v = v.rotate(-self.eye.angle)
        return EventAdjustment.Param(v.x, v.y)


class ActionScale(Action):
    def __init__(self, eye: Eye) -> None:
        self.eye = eye
        self.move_amount = 0.01
        super().__init__()

    def action(self, event: tk.Tk):
        event_adjustment = self.event(event)
        self.eye.scale_width += event_adjustment.change_scale_width
        self.eye.scale_height += event_adjustment.change_scale_height

    def event(self, event: tk.Tk) -> EventAdjustment.Param:
        change_scale_width: float = 0.0
        change_scale_height: float = 0.0

        if event.keysym == "Right":
            change_scale_width += self.move_amount
        elif event.keysym == "Left":
            change_scale_width -= self.move_amount
        elif event.keysym == "Up":
            change_scale_height += self.move_amount
        elif event.keysym == "Down":
            change_scale_height -= self.move_amount

        return EventAdjustment.Param(change_scale_width=change_scale_width, change_scale_height=change_scale_height)


class ActionAngle(Action):
    def __init__(self, eye: Eye) -> None:
        self.eye = eye
        self.move_amount = 1
        super().__init__()

    def action(self, event: tk.Tk):
        if event.keysym == "Right" or event.keysym == "Up":
            self.eye.angle += self.move_amount
        elif event.keysym == "Left" or event.keysym == "Down":
            self.eye.angle -= self.move_amount

    def event(self, event: tk.Tk) -> EventAdjustment.Param:
        change_angle: float = 0.0

        if event.keysym == "Right" or event.keysym == "Up":
            change_angle += self.move_amount
        elif event.keysym == "Left" or event.keysym == "Down":
            change_angle -= self.move_amount

        return EventAdjustment.Param(change_angle=change_angle)
