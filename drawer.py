# TODO:再描画の必要のない時は再描画しないようにする
class Drawer():
    def __init__(self) -> None:
        self.needs_draw = False
