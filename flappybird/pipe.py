from flappybird.window import Window
from PIL import Image
import random


class PipeSegment(Window):
    def __init__(self, height: int, flipped: bool) -> None:
        image = Image.open("assets/pipe.png")
        base = Image.new("RGBA", (100, height))

        top = image.crop((0, 0, 32, 19))
        top = top.resize(
            (100, int(100 / top.width * top.height)), Image.NEAREST)

        bottom = image.crop((0, 19, 32, 20))
        bottom = bottom.resize((100, height - top.height), Image.NEAREST)
        if flipped:
            top = top.transpose(Image.FLIP_TOP_BOTTOM)
            base.paste(top, (0, base.height - top.height))
            base.paste(bottom, (0, 0))
        else:
            base.paste(top, (0, 0))
            base.paste(bottom, (0, top.height))

        super().__init__(0, 0, base, "Pipe")

    def collide(self, rect: tuple[int, int, int, int]) -> bool:
        rect_left, rect_top, rect_right, rect_bottom = rect
        return (self.x < rect_right and
                self.x + self.width() > rect_left and
                self.y < rect_bottom and
                self.y + self.height() > rect_top)


class Pipe:
    def __init__(self, screenheight: int) -> None:
        gap = 500
        top_height = random.randint(0, screenheight // 2 - 300) + gap // 2
        bottom_height = screenheight - top_height - gap

        self.top_seg = PipeSegment(top_height, True)
        self.bottom_seg = PipeSegment(bottom_height, False)

        screenwidth = self.top_seg.window.winfo_screenwidth()
        self.top_seg.move_abs(screenwidth - self.top_seg.width(), 0)

        self.bottom_seg.move_abs(
            screenwidth - self.bottom_seg.width(), screenheight - self.bottom_seg.height())

    def update(self) -> None:
        self.top_seg.move_rel(-10, 0)
        self.bottom_seg.move_rel(-10, 0)

    def delete(self):
        self.top_seg.window.destroy()
        self.bottom_seg.window.destroy()

    def collide(self, rect: tuple[int, int, int, int]) -> bool:
        return self.top_seg.collide(rect) or self.bottom_seg.collide(rect)
