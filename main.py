import tkinter as tk
from PIL import Image, ImageTk
import random

class ArkanoidGame:
    def __init__(self):
        self.root = tk.Tk()
        self.create_canvas()

        self.width = 400
        self.height = 300

        self.game_running = True
        self.life = 1
        self.score = 0

        self.display_interface()
        self.create_bricks()
        self.create_ball()
        self.create_pad()

        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.focus_set()

        self.keys_pressed = set()

        self.game_loop()
        self.window_in_the_center()


    def window_in_the_center(self):
        x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry(f'{self.width}x{self.height}+{x}+{y}')


    def create_canvas(self):
        image = Image.open("images/background.jpg")
        self.bg_image = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="white")
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")


    def create_bricks(self):
        self.bricks = []
        bricks_weidth = 53
        bricks_height = 10
        bricks_padding = 3

        for row in range(6):
            for col in range(7):
                x1 = col * (bricks_weidth + bricks_padding) + bricks_padding + 5
                y1 = row * (bricks_height + bricks_padding) + 20
                x2 = x1 + bricks_weidth
                y2 = y1 + bricks_height

                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    tags = "bricks",
                    fill = "tan",
                    outline = "tan2"
                )
                self.bricks.append(brick)


    def create_pad(self):
        self.pad_width = 70
        self.pad_height = 6
        self.pad_x = self.width // 2 - self.pad_width // 2
        self.pad_y = self.height - 20
        self.pad_speed = 5

        self.pad = self.canvas.create_rectangle(
            self.pad_x,
            self.pad_y,
            self.pad_x + self.pad_width,
            self.pad_y + self.pad_height,
            fill = "cornsilk4",
            outline = "blueviolet",
            tags = "pad"
        )

