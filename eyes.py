
from __future__ import annotations
from eyelids import Eyelids
from irises import PygameIrises
import pygame
from typing import Optional
import logging
import os
import json

logger = logging.getLogger()


class Eye():
    def __init__(self, origin_x: int = 0, origin_y: int = 0) -> None:
        self.origin_x: int = origin_x
        self.origin_y: int = origin_y
        self.scale_width: float = 1
        self.scale_height: float = 1
        self.angle: float = 0

    def dump(self) -> dict:
        return {
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


class Eyes():
    def __init__(self, width: Optional[int] = None, height: Optional[int] = None) -> None:

        self.left = Eye()
        self.right = Eye()
        self.irises = PygameIrises(width, height)
        self.eyelids = Eyelids()

    def update(self, delta_time: float):

        for eye, iris in zip(
            [self.left, self.right],
                [self.irises.left, self.irises.right]):
            iris.origin_x = eye.origin_x
            iris.origin_y = eye.origin_y
            iris.scale_width = eye.scale_width
            iris.scale_height = eye.scale_height
            iris.angle = eye.angle

        self.eyelids.left.angle = self.left.angle
        self.eyelids.right.angle = self.right.angle
        self.irises.update(delta_time)
        self.eyelids.update(delta_time)

    def draw(self,
             left_screen: pygame.Surface,
             right_screen: pygame.Surface):
        self.irises.draw(left_screen, right_screen)
        self.eyelids.draw(left_screen, right_screen)

    def dump(self) -> dict:
        return {
            "eyes": {
                "right": self.right.dump(),
                "left": self.left.dump()},
            "irises": self.irises.dump()
        }

    def load(self, data: dict):
        eyes = data["eyes"]
        self.right.load(eyes["right"])
        self.left.load(eyes["left"])

        self.irises.load(data["irises"])

    def save_to_config(self, file_path: str = "./config.json"):
        with open(file_path, "w") as f:
            json.dump(self.dump(), f)
        logger.info("Save data. file path=%s", file_path)

    def load_from_config(self, file_path: str = "./config.json"):
        if not os.path.isfile(file_path):
            return
        with open(file_path, "r") as f:
            data = json.load(f)
        try:
            self.load(data)
        except Exception as e:
            logger.error("Failed load. %s", e)
        else:
            logger.info("Load data. file path=%s", file_path)
