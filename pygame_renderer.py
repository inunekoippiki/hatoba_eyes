import pygame
from pygame.locals import *
from eyes import Eyes
import logging
from screeninfo import get_monitors
import api
import queue
import threading
import argparse
import time
from const import WHERE_EYE_COLOR

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--fullscreen', type=bool, default=False)
parser.add_argument('--display', type=int, default=0)


args = parser.parse_args()

logger = logging.getLogger()

pygame.init()

monitor = get_monitors()[args.display]

width = monitor.width
height = monitor.height

screen = pygame.display.set_mode((width, height))

if not pygame.display.is_fullscreen() and args.fullscreen:
    pygame.display.toggle_fullscreen()


def create_eyes(one_screen: tuple):
    eyes = Eyes(*one_screen)
    eyes.load_from_config()
    return eyes


def run_api():
    api.run()


one_screen = (width/2, height)
left_screen = pygame.Surface(one_screen)
right_screen = pygame.Surface(one_screen)
eyes = create_eyes(one_screen)

api_thread = threading.Thread(target=run_api)
api_thread.start()

is_exit = False
start_time = time.time()

while not is_exit:
    end_time = time.time()
    delta_time = end_time - start_time
    start_time = end_time
    while True:
        try:
            event = api.events.get_nowait()
            event.exec(eyes)
        except queue.Empty:
            break

    left_screen.fill(WHERE_EYE_COLOR)
    right_screen.fill(WHERE_EYE_COLOR)
    eyes.update(delta_time)
    eyes.draw(left_screen, right_screen)
    screen.blit(left_screen, pygame.Rect(0, 0, *one_screen))
    screen.blit(right_screen, pygame.Rect(width/2, 0, *one_screen))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            is_exit = True
