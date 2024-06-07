import tkinter as tk
from PIL import Image, ImageTk


class Window:
    def __init__(self, x: int, y: int, image: Image, title: str = "") -> None:
        self.x, self.y = x, y
        self.window = tk.Toplevel()
        self.window.title(title)
        self.window.attributes("-topmost", True)
        self.updatePos()

        self.image = image
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.label = tk.Label(self.window, image=self.tk_image)
        self.label.pack()

    def width(self) -> None:
        return self.image.size[0] + 8

    def height(self) -> None:
        return self.image.size[1] + 38

    def init(self) -> None:
        self.window.mainloop()

    def updatePos(self) -> None:
        self.window.geometry(f"+{int(self.x)}+{int(self.y)}")

    def move_abs(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.updatePos()

    def move_rel(self, x: int, y: int) -> None:
        self.x += x
        self.y += y
        self.updatePos()
 