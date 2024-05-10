import tkinter as tk
import tkinter.ttk as ttk
from logger import GUILogHandler
import logging
from screeninfo import get_monitors
import json
from debug_monitor_window import DebugMonitorWindow
import threading
import time
import select_dialog
import controller
from motion_controller import MonitonController
import container
from irises import Irises
from eyes import Eyes
from detector import Detector
from motion import MotionManager
import pygame
from typing import Optional
from const import WHERE_EYE_COLOR

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def begin_action(event: tk.Event):
    pass


def update_action(event: tk.Event):

    end_x = max(min(width, event.x), 0)
    end_y = max(min(height, event.y), 0)

    debug_monitor.print("canvas_x", end_x)
    debug_monitor.print("canvas_x", end_y)

    motion_controller.direction(
        int(event.x - width / 2),
        int(event.y - height / 2),
    )


def release_action(event: tk.Event):
    pass


def select_eyes_set(irises: Irises, id: str):
    irises.select(id)


def add_eyes_set(irises: Irises, textbox: tk.Entry, eyes_set_selectbox: ttk.Combobox):
    irises.eyes_set.add(textbox.get(), irises)
    eyes_set_selectbox.config(values=list(irises.eyes_set.file_path.keys()))


def link_pygame_eyes(display: int = 0, fullscreen: bool = True):
    pygame.init()
    screen = pygame.display.set_mode((width, height), display=display)

    if not pygame.display.is_fullscreen() and fullscreen:
        pygame.display.toggle_fullscreen()
    one_screen = (width/2, height)
    left_screen = pygame.Surface(one_screen)
    right_screen = pygame.Surface(one_screen)
    is_exit = False

    start_time = time.time()

    while not is_exit:
        end_time = time.time()
        delta_time = end_time - start_time
        start_time = end_time

        if detector and detector.is_detect():
            target_x, target_y = detector.primary_target()
            tx = -(target_x - (detector.width * 0.5)) / detector.width
            ty = (target_y - (detector.height * 0.5)) / detector.height
            [e.set_target(tx, ty) for e in direction_target_motions]
            debug_monitor.print("tx", tx)
            debug_monitor.print("ty", ty)

        eyes.update(delta_time)
        motion_manager.update(delta_time)
        motion_controller.update(delta_time)
        left_screen.fill(WHERE_EYE_COLOR)
        right_screen.fill(WHERE_EYE_COLOR)
        irises.draw(left_screen, right_screen)
        eyes.draw(left_screen, right_screen)
        screen.blit(left_screen, pygame.Rect(0, 0, *one_screen))
        screen.blit(right_screen, pygame.Rect(width/2, 0, *one_screen))
        pygame.display.update()

        # 終了イベントを確認 --- (*5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                is_exit = True


root = tk.Tk()
root.title("画像描画")

handler = GUILogHandler(root, logging.DEBUG)
logger.addHandler(handler)

debug_monitor = DebugMonitorWindow(root)
container.debug_monitor_window = debug_monitor
monitors = get_monitors()
logger.info("Get display infomation.")
logger.info(
    json.dumps(monitors, default=lambda o: o.__dict__,
               sort_keys=True, indent=4)
)

select_monitor = select_dialog.SelectDialog(
    root,
    "ディスプレイ選択：アイに使用するディスプレイを選択してください",
    {monitor.name: i for i, monitor in enumerate(monitors)},
    {
        monitor.name: f"{('primary' if monitor.is_primary else 'sub')}:"
        f"{monitor.width}*{monitor.height}"
        for i, monitor in enumerate(monitors)
    },
)

eyes_monitor_idx = select_monitor.result
logger.info("eyes_monitor=%s", eyes_monitor_idx)
eyes_monitor = monitors[eyes_monitor_idx]

width = 960
height = 480
display_size = (width, height)

canvas = tk.Canvas(
    root, width=display_size[0], height=display_size[1], bg="white")
canvas.pack()

canvas.bind("<ButtonPress-1>", begin_action)
canvas.bind("<Button1-Motion>", update_action)
canvas.bind("<ButtonRelease-1>", release_action)

eyes = Eyes(*display_size)
irises = eyes.irises
controll = controller.Controller(root, canvas, eyes)
eyes.load_from_config()

# UI 操作

operation_frame = tk.Frame(root)
save_button = tk.Button(
    operation_frame, text="保存", command=lambda: eyes.save_to_config()
)
save_button.pack(side=tk.LEFT, anchor=tk.CENTER)
load_button = tk.Button(operation_frame, text="読込",
                        command=lambda: eyes.load_from_config())
load_button.pack(side=tk.LEFT, anchor=tk.CENTER)
reset_button = tk.Button(operation_frame, text="リセット",
                         command=lambda: eyes.irises.reset())
reset_button.pack(side=tk.LEFT, anchor=tk.CENTER)
reset_button = tk.Button(
    operation_frame, text="左右入れ替え", command=lambda: eyes.irises.switch()
)
reset_button.pack(side=tk.LEFT, anchor=tk.CENTER)

operation_frame.pack(side=tk.TOP, anchor=tk.N)

# UI アイ画像セット
eyes_set_frame = tk.Frame(root)

currnt_eyes_set = None
eyes_set_selectbox = ttk.Combobox(
    eyes_set_frame,
    values=list(irises.eyes_set.file_path.keys()),
    textvariable=currnt_eyes_set,
)
eyes_set_selectbox.bind(
    "<<ComboboxSelected>>",
    lambda event: select_eyes_set(irises, eyes_set_selectbox.get()),
)
eyes_set_selectbox.pack(side=tk.LEFT, anchor=tk.CENTER)

eyes_set_id_input = tk.Entry(eyes_set_frame)
eyes_set_id_input.pack(side=tk.LEFT, anchor=tk.CENTER)

eyes_set_add_button = tk.Button(
    eyes_set_frame,
    text="追加",
    command=lambda: add_eyes_set(
        irises, eyes_set_id_input, eyes_set_selectbox),
)
eyes_set_add_button.pack(side=tk.LEFT, anchor=tk.CENTER)


eyes_set_frame.pack(side=tk.TOP, anchor=tk.N)

motion_manager = MotionManager()

motion_controller = MonitonController(root, eyes)

irises.right.motion = motion_controller.eye_direction_motion_right
irises.left.motion = motion_controller.eye_direction_motion_left

# eyes.irises.right.motion = motion_manager.create_motion(
#     IrisDirectionTargetMotion)
# eyes.irises.left.motion = motion_manager.create_motion(
#     IrisDirectionTargetMotion)
# direction_target_motions = [eyes.irises.right.motion, eyes.irises.left.motion]
direction_target_motions = []

# detector: Optional[Detector] = Detector()
# detector.start()
detector: Optional[Detector] = None

t_link_pygame_eyes = threading.Thread(
    target=lambda: link_pygame_eyes(eyes_monitor_idx, False))
t_link_pygame_eyes.start()

# メインループの開始
root.mainloop()
