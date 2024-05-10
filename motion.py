import math
import random
from typing import TypeVar


class Motion:
    def __init__(self) -> None:
        self.is_deleted = False

    def delete(self):
        self.is_deleted = True

    def update(self, delta_time: float):
        pass


class EyelidMotion(Motion):
    def __init__(self) -> None:
        pass

    def height(self) -> float:
        pass


class EyelidBlinkMotion(EyelidMotion):
    def __init__(self, ) -> None:
        super().__init__()
        self.time = 0.0
        self.time_max = math.asin(1)*2
        self.speed = 6.0
        self.scale_height = 0.0

    def update(self, delta_time: float):
        self.time += delta_time * self.speed
        self.time = min(self.time, self.time_max)
        self.scale_height = abs(math.sin(self.time))

    def get_scale_height(self) -> float:
        return self.scale_height

    def blink(self):
        self.time = 0.0


class EyelidsAutoBlinkMotion(Motion):
    def __init__(self, ) -> None:
        super().__init__()
        self.base_interval = 5.0
        self.interval_range = 2.0
        self.interval = self.decide_interval()
        self.interval_count = 0.0
        self.double_blink_rate = 0.1
        self.blink_time = 0.6

        self.blink = False

    def update(self, delta_time: float):
        self.interval_count += delta_time
        if self.interval_count >= self.interval:
            self.interval_count = 0.0
            self.blink = True
            if random.random() < self.double_blink_rate:
                self.interval = self.blink_time
            else:
                self.interval = self.decide_interval()

    def decide_interval(self):
        return self.base_interval + self.interval_range * random.random()

    def is_blink(self):
        return self.blink

    def blinked(self):
        self.blink = False


class IrisMotion(Motion):
    def __init__(self) -> None:
        super().__init__()

    def relative_position(self) -> tuple[float, float]:
        pass


class IrisDirectionMotion(IrisMotion):
    def __init__(self) -> None:
        super().__init__()
        self.angle = 0.0
        self.amount = 1.0
        self.x = 0.0
        self.y = 0.0

    def update(self, delta_time: float):
        pass

    def set_target(self, x: float, y: float) -> None:
        self.x = x * self.amount
        self.y = y * self.amount

    def relative_position(self) -> tuple[float, float]:
        return (self.x, self.y)


class IrisDirectionTargetMotion(IrisMotion):
    def __init__(self) -> None:
        super().__init__()
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0
        self.target_y = 0
        self.x_range = 150
        self.y_range = 100
        self.speed = 1.0

    def update(self, delta_time: float):
        delta_speed = min(self.speed * delta_time, 1.0)
        self.x = self.x * (1 - delta_speed) + \
            self.target_x * self.x_range * delta_speed
        self.y = self.y * (1 - delta_speed) + \
            self.target_y * self.y_range * delta_speed

    def set_target(self, x: float, y: float) -> None:
        self.target_x = x
        self.target_y = y

    def relative_position(self) -> tuple[float, float]:
        return (self.x, self.y)


T = TypeVar("T")


class MotionManager:
    def __init__(self) -> None:
        self.l: list[Motion] = []

    def create_motion(self, t: type[T], *args, **kwargs) -> T:
        motion = t(*args, **kwargs)
        self.l.append(motion)
        return motion

    def update(self, delta_time: float):
        self.l = list(filter(lambda x: not x.is_deleted, self.l))
        for e in self.l:
            e.update(delta_time)
