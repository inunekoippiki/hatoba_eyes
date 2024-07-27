from eyes import Eyes, Eye


class Event():
    def exec(self, eyes: Eyes):
        pass


class EventAdjustment(Event):
    class Param():
        def __init__(self,
                     change_x: float = 0.0,
                     change_y: float = 0.0,
                     change_scale_width: float = 0.0,
                     change_scale_height: float = 0.0,
                     change_angle: float = 0.0) -> None:
            self.change_x = change_x
            self.change_y = change_y
            self.change_scale_width = change_scale_width
            self.change_scale_height = change_scale_height
            self.change_angle = change_angle

    def __init__(self, left: Param = Param(), right: Param = Param()) -> None:
        self.left = left
        self.right = right

    def exec(self, eyes: Eyes):
        adjustment(eyes.left, self.left)
        adjustment(eyes.right, self.right)


class EventEyeDirection(Event):
    class Param():
        def __init__(self,
                     x: float = 0.0,
                     y: float = 0.0):
            self.x = x
            self.y = y

        def vec2(self):
            return (self.x, self.y)

    def __init__(self,
                 left: Param = Param(), right: Param = Param()) -> None:
        self.left = left
        self.right = right

    def exec(self, eyes: Eyes):
        irises = eyes.irises
        irises.left.set_target(*self.left.vec2())
        irises.right.set_target(*self.right.vec2())


class EventChangeEyeType(Event):
    def __init__(self, id: str) -> None:
        self.id = id

    def exec(self, eyes: Eyes):
        irises = eyes.irises
        irises.eyes_set.select(self.id, eyes.irises)


class EventSynchronise(Event):
    class Param():
        def __init__(self,
                     file_path: str = "",
                     origin_x: float = 0.0,
                     origin_y: float = 0.0,
                     scale_width: float = 0.0,
                     scale_height: float = 0.0,
                     angle: float = 0.0):
            self.file_path = file_path
            self.origin_x = origin_x
            self.origin_y = origin_y
            self.scale_width = scale_width
            self.scale_height = scale_height
            self.angle = angle

    def __init__(self,
                 left: Param = Param(),
                 right: Param = Param(),
                 enable_save: bool = False) -> None:
        self.left = left
        self.right = right
        self.enable_save = enable_save

    def exec(self, eyes: Eyes):
        for e, param in zip([eyes.left, eyes.right], [self.left, self.right]):
            e.origin_x = param.origin_x
            e.origin_y = param.origin_y
            e.scale_width = param.scale_width
            e.scale_height = param.scale_height
            e.angle = param.angle
        irises = eyes.irises
        for e, param in zip([irises.left, irises.right], [self.left, self.right]):
            e.read_image(e.file_path)
        if self.enable_save:
            eyes.save_to_config()


class EventSave(Event):
    def __init__(self) -> None:
        pass

    def exec(self, eyes: Eyes):
        eyes.save_to_config()


class EventBlink(Event):
    def __init__(self) -> None:
        pass

    def exec(self, eyes: Eyes):
        eyes.eyelids.blink()


class EventEnableBlink(Event):
    def __init__(self, enable: bool) -> None:
        self.enable = enable

    def exec(self, eyes: Eyes):
        eyes.eyelids.enable_blink = self.enable


class EventUpload(Event):
    def __init__(self, data: dict) -> None:
        self.data = data

    def exec(self, eyes: Eyes):
        eyes.eyelids.blink()

class EventEnableIrisesRandomDirection(Event):
    def __init__(self, enable: bool, kwargs:dict = {}) -> None:
        self.enable = enable
        self.kwargs = kwargs

    def exec(self, eyes: Eyes):
        motion = eyes.irises.random_direction_target_motion
        eyes.irises.enable_random_eyes_direction = self.enable
        
        if "base_interval" in self.kwargs:
            motion.base_interval = self.kwargs["base_interval"]
        if "interval_range" in self.kwargs:
            motion.interval_range = self.kwargs["interval_range"]
            
        if "rx_max" in self.kwargs:
            motion.rx_max = self.kwargs["rx_max"]
        if "rx_min" in self.kwargs:
            motion.rx_min = self.kwargs["rx_min"]
        if "ry_max" in self.kwargs:
            motion.ry_max = self.kwargs["ry_max"]
        if "ry_min" in self.kwargs:
            motion.ry_min = self.kwargs["ry_min"]
            
        if "lx_max" in self.kwargs:
            motion.lx_max = self.kwargs["lx_max"]
        if "lx_min" in self.kwargs:
            motion.lx_min = self.kwargs["lx_min"]
        if "ly_max" in self.kwargs:
            motion.ly_max = self.kwargs["ly_max"]
        if "ly_min" in self.kwargs:
            motion.ly_min = self.kwargs["ly_min"]


def adjustment(eye: Eye, event: EventAdjustment.Param):
    eye.origin_x += event.change_x
    eye.origin_y += event.change_y
    eye.scale_width += event.change_scale_width
    eye.scale_height += event.change_scale_height
    eye.angle += event.change_angle
