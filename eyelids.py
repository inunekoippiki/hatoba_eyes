import pygame
from motion import EyelidBlinkMotion, EyelidsAutoBlinkMotion


class Eyelid():
    def __init__(self) -> None:
        self.file_path = "./resource/blink.png"
        self.origin_image = pygame.image.load(self.file_path)

        self.x = 0
        self.y = 0
        self.angle = 0.0

        self.motion = EyelidBlinkMotion()

    def update(self, delta_time: float):
        self.motion.update(delta_time)

    def draw(self, screen: pygame.Surface):
        rotate_image = pygame.transform.rotate(self.origin_image, self.angle)
        center_rect = rotate_image.get_rect(
            center=self.origin_image.get_rect(center=(self.origin_image.get_width()/2,
                                                      self.origin_image.get_height()/2)).center)
        rect = center_rect.move(
            pygame.Vector2(0, -self.origin_image.get_height() * (1-self.motion.get_scale_height())).rotate(-self.angle))
        screen.blit(rotate_image, rect)

    def blink(self):
        self.motion.blink()


class Eyelids():
    def __init__(self) -> None:
        self.left = Eyelid()
        self.right = Eyelid()
        self.motion = EyelidsAutoBlinkMotion()
        self.enable_blink = False

    def update(self, delta_time: float):
        self.motion.update(delta_time)
        self.left.update(delta_time)
        self.right.update(delta_time)
        if self.motion.is_blink() and self.enable_blink:
            self.motion.blinked()
            self.blink()

    def draw(self,
             left_screen: pygame.Surface,
             right_screen: pygame.Surface):
        self.left.draw(left_screen)
        self.right.draw(right_screen)

    def blink(self):
        self.left.blink()
        self.right.blink()
