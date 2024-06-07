import tkinter as tk
from flappybird.bird import Bird
from flappybird.pipe import Pipe
from pynput import keyboard


class App:
    def __init__(self) -> None:
        # Create the root window
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.geometry("+0+0")

        self._score = 0
        self.score_label = tk.Label(
            self.root, text=f"Score: {self.score}", font=("Helvetica", 24))
        self.score_label.pack()

        self.bird = Bird(100, 0)
        self.pipes: list[Pipe] = []

        # Start the global keyboard event listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value: int) -> None:
        self._score = value
        self.score_label.config(text=f"Score: {self._score}")
        self.score_label.update()

    def run(self) -> None:
        # Start the first loop instance, which will then instanciate itself after it ends
        self._loop()

        # Create the loop that creates pipes
        self._pipe_loop()

        self.bird.init()

    def reset(self) -> None:
        for pipe in self.pipes:
            pipe.delete()
        self.pipes.clear()
        self.bird.yv = 0
        self.bird.y = 0
        self.score = 0

    def _loop(self) -> None:
        self.bird.gravity()

        if self.bird.y + self.bird.height() > self.root.winfo_screenheight() - 40:
            self.reset()

        for pipe in self.pipes:
            # Move the pipes and delete them when they get out of bounds
            pipe.update()
            if pipe.top_seg.x < 0:
                pipe.delete()
                self.pipes.remove(pipe)
                self.score += 1

            # Check collision with the bird
            collision = pipe.collide(
                (self.bird.x, self.bird.y, self.bird.x + self.bird.width(), self.bird.y + self.bird.height()))
            if collision:
                self.reset()
                print("Player died")

        # Create a new loop instance
        self.root.after(int(1/60*1000), self._loop)

    def _pipe_loop(self) -> None:
        self.pipes.append(Pipe(self.root.winfo_screenheight() - 40))
        self.root.after(2000, self._pipe_loop)

    def on_press(self, key: keyboard.Key) -> None:
        # Make the bird jump
        if key == keyboard.Key.space:
            self.bird.yv = -30


if __name__ == "__main__":
    app = App()
    app.run()
