import tkinter as tk

from typing import Optional
from PIL import ImageTk, Image
from motion import IrisDirectionMotion, IrisDirectionTargetMotion,IrisesRandomDirectionMotion
import logging
import pygame
import json
import os

logger = logging.getLogger()


class Iris:
    def __init__(self, origin_x: int = 0, origin_y: int = 0) -> None:
        self.default_origin_x = origin_x
        self.default_origin_y = origin_y

        self.file_path: Optional[str] = None
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
        self.scale_width: float = 1
        self.scale_height: float = 1
        self.angle: float = 0
        
        self.motion: Optional[IrisDirectionMotion] = IrisDirectionTargetMotion(
        )

    def dump(self) -> dict:
        return {
            "file_path": self.file_path,
            "origin_x": self.origin_x,
            "origin_y": self.origin_y,
            "scale_width": self.scale_width,
            "scale_height": self.scale_height,
            "angle": self.angle,
        }

    def load(self, data: dict):
        self.origin_x = data["origin_x"]
        self.origin_y = data["origin_y"]
        self.scale_width = data["scale_width"]
        self.scale_height = data["scale_height"]
        self.angle = data["angle"]

    def read_image(self, file_path: str):
        self.file_path = file_path

    def update(self, delta_time: float):
        if self.motion:
            self.motion.update(delta_time)

    def draw(self, *args, **kwargs):
        pass

    def reset(self):
        self.origin_x = self.default_origin_x
        self.origin_y = self.default_origin_y
        self.scale_width = 1
        self.scale_height = 1
        self.angle = 0

    def set_target(self, x: float, y: float):
        if self.motion:
            self.motion.set_target(x, y)


class PILIris(Iris):
    def __init__(self, origin_x: int = 0, origin_y: int = 0) -> None:
        super().__init__(origin_x, origin_y)
        self.origin_image: Optional[Image.Image] = None
        self.image: Optional[Image.Image] = None

    def load(self, data: dict):
        self.read_image(data["file_path"])
        super().load(data)

    def read_image(self, file_path: str):
        self.origin_image = Image.open(file_path)
        super().read_image(file_path)

    def draw(self, canvas: tk.Canvas):
        if self.origin_image is None:
            return
        self.image = self.origin_image.rotate(self.angle, expand=True)
        w, h = self.image.size
        self.image = self.image.resize(
            (int(w * self.scale_width), int(h * self.scale_height))
        )
        self.tk_image = ImageTk.PhotoImage(self.image)
        if self.motion:
            canvas.create_image(
                self.origin_x + self.motion.x,
                self.origin_y + self.motion.y,
                anchor=tk.CENTER,
                image=self.tk_image,
            )
        else:
            canvas.create_image(
                self.origin_x, self.origin_y, anchor=tk.CENTER, image=self.tk_image
            )


class PygameIris(Iris):
    def __init__(self, origin_x: int = 0, origin_y: int = 0) -> None:
        super().__init__(origin_x, origin_y)
        self.origin_image: pygame.Surface = None

    def load(self, data: dict):
        self.read_image(data["file_path"])
        super().load(data)

    def read_image(self, file_path: str):
        self.origin_image = pygame.image.load(file_path)
        super().read_image(file_path)

    def draw(self, screen: pygame.Surface):
        scale_image = pygame.transform.smoothscale(
            self.origin_image, (self.origin_image.get_width() * self.scale_width, self.origin_image.get_height()*self.scale_height))
        rotate_image = pygame.transform.rotozoom(scale_image, self.angle, 1.0)
        center_rect = rotate_image.get_rect(
            center=self.origin_image.get_rect(center=(self.origin_x, self.origin_y)).center)
        if self.motion:
            center_rect.move_ip(pygame.Vector2(
                self.motion.x, self.motion.y).rotate(-self.angle))
        screen.blit(rotate_image, center_rect)


class Irises:
    def __init__(
        self,
    ) -> None:
        self.right: Iris
        self.left: Iris
        self.eyes_set = EyesSet()

        self.enable_random_eyes_direction = True
        self.random_direction_target_motion = IrisesRandomDirectionMotion()
        
    def update(self, delta_time: float):
        self.right.update(delta_time)
        self.left.update(delta_time)
        if(self.enable_random_eyes_direction):
            self.random_direction_target_motion.update(delta_time)
            r,l = self.random_direction_target_motion.relative_position()
            self.right.set_target(*r)
            self.left.set_target(*l)

    def draw(self, canvas: tk.Canvas):
        self.right.draw(canvas)
        self.left.draw(canvas)

    def dump(self) -> dict:
        return {
            "right": self.right.dump(),
            "left": self.left.dump(),
            "eyes_set": self.eyes_set.dump(),
        }

    def load(self, data: dict):
        self.right.load(data["right"])
        self.left.load(data["left"])
        self.eyes_set.load(data["eyes_set"])

    def select(self, id: str):
        self.eyes_set.select(id, self)

    def reset(self):
        self.right.reset()
        self.left.reset()


class PILIrises(Irises):
    def __init__(self, width: Optional[int] = None, height: Optional[int] = None) -> None:
        super().__init__()
        if width and height:
            self.right: PILIris = PILIris(width * 0.75, height / 2)
            self.left: PILIris = PILIris(width * 0.25, height / 2)
        else:
            self.right: PILIris = PILIris()
            self.left: PILIris = PILIris()

    def draw(self, canvas: tk.Canvas):
        self.right.draw(canvas)
        self.left.draw(canvas)


class PygameIrises(Irises):
    def __init__(self, width: Optional[int] = None, height: Optional[int] = None) -> None:
        super().__init__()
        if width and height:
            self.right: PygameIris = PygameIris(width / 2, height / 2)
            self.left: PygameIris = PygameIris(width / 2, height / 2)
        else:
            self.right: PygameIris = PygameIris()
            self.left: PygameIris = PygameIris()

    def switch(self):
        right = self.right.file_path
        left = self.left.file_path
        self.right.read_image(left)
        self.left.read_image(right)

    def draw(self,
             left_screen: pygame.Surface,
             right_screen: pygame.Surface):
        self.right.draw(right_screen)
        self.left.draw(left_screen)


class EyesSet:
    def __init__(self) -> None:
        self.file_path: dict[str, tuple[str, str]] = {}

    def add(self, id: str, irises: Irises):
        self.file_path[id] = (irises.right.file_path, irises.left.file_path)

    def select(self, id: str, irises: Irises):
        if id not in self.file_path:
            logger.warning("Unknown id.id=%s", id)
            return
        right, left = self.file_path[id]
        irises.right.read_image(right)
        irises.left.read_image(left)

    def dump(self) -> None:
        return self.file_path

    def load(self, obj) -> None:
        self.file_path = obj
