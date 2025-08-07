import tkinter as tk
from PIL import Image, ImageTk
import random

class PlayingField:
    def __init__(self):
        self.root = tk.Tk()
        self.create_canvas()

        self.width = 400
        self.height = 300

        self.create_bricks()
        self.create_ball()
        self.create_pad()

        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.focus_set()

        self.keys_pressed = set()

        self.game_loop()
        self.window_in_the_center()
        self.root.mainloop()

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
        bricks_padding = 2

        for row in range(4):
            for col in range(7):
                x1 = col * (bricks_weidth + bricks_padding) + bricks_padding + 5
                y1 = row * (bricks_height + bricks_padding) + 20
                x2 = x1 + bricks_weidth
                y2 = y1 + bricks_height

                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill = "tan",
                    outline = "tan2"
                )
                self.bricks.append(brick)

    def create_pad(self):
        self.pad_width = 70
        self.pad_height = 5
        self.pad_x = self.width // 2 - self.pad_width // 2
        self.pad_y = self.height - 20
        self.pad_speed = 5

        self.pad = self.canvas.create_rectangle(
            self.pad_x,
            self.pad_y,
            self.pad_x + self.pad_width,
            self.pad_y + self.pad_height,
            fill = "cornsilk4",
            outline = "blueviolet"
        )

    def create_ball(self):
        self.ball_radius = 4
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2 + 50
        self.ball_dx = random.choice([-3,3]) # speed
        self.ball_dy = -3 # speed

        self.ball = self.canvas.create_oval(
            self.ball_x - self.ball_radius,
            self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius,
            self.ball_y + self.ball_radius,
            fill = "darkorange",
            outline = "deeppink1"
        )

    def key_press(self, event):
        self.keys_pressed.add(event.keysym.lower())

    def key_release(self, event):
        self.keys_pressed.discard(event.keysym.lower())

    def move_pad(self):
        if "a" in self.keys_pressed:
            if self.pad_x > 0:
                self.pad_x -= self.pad_speed

        if "d" in self.keys_pressed:
            if self.pad_x < self.width - self.pad_width:
                self.pad_x += self.pad_speed

        self.canvas.coords(
            self.pad,
            self.pad_x,
            self.pad_y,
            self.pad_x + self.pad_width,
            self.pad_y + self.pad_height
        )

    def move_ball(self):
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        if self.ball_x <= self.ball_radius or self.ball_x >= self.width - self.ball_radius:
            self.ball_dx = -self.ball_dx # Can be replaced with ( *= -1 )

        if self.ball_y <= self.ball_radius:
            self.ball_dy = -self.ball_dy # Can be replaced with ( *= -1 )

        # Bounce off the platform
        if (
                self.ball_x > self.pad_x
                and self.ball_x + self.ball_radius < self.pad_x + self.pad_width
                and self.ball_y  < self.pad_y + self.height
                and self.ball_y + self.ball_radius >= self.pad_y
        ):
            hit_pos = (self.ball_x - self.pad_x) / self.pad_width
            self.ball_dx = (hit_pos - 0.5) * 6
            self.ball_dy = -abs(self.ball_dy)

        # Removes brick on collision
        for brick in self.bricks[:]:
            brick_coords = self.canvas.coords(brick)

            if not brick_coords:
                continue

            x1, y1, x2, y2 = brick_coords
            if (
                    x1 <= self.ball_x <= x2
                    and self.ball_y > y1
                    and self.ball_y + self.ball_radius >= y2
            ):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                # Bounce
                self.ball_dy = -self.ball_dy

        self.canvas.coords(
        self.ball,
        self.ball_x - self.ball_radius,
        self.ball_y - self.ball_radius,
        self.ball_x + self.ball_radius,
        self.ball_y + self.ball_radius
        )



    def game_loop(self):
        self.move_ball()
        self.move_pad()
        self.root.after(30, self.game_loop)

PlayingField()

