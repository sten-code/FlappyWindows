import tkinter as tk
from PIL import Image
from flappybird.window import Window


class Bird(Window):
    def __init__(self, x: int, y: int) -> None:
        image = Image.open("assets/bird.png")
        ratio = image.size[0] / image.size[1]
        image = image.resize((int(ratio * 100), 100), Image.NEAREST)

        super().__init__(x, y, image, "Flappy Bird")
        self.xv, self.yv = 0, 0

    def gravity(self) -> None:
        self.yv += 2
        self.move_rel(0, self.yv)

