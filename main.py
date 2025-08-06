import tkinter as tk
from PIL import Image, ImageTk


class PlayingField:
    def __init__(self):
        self.root = tk.Tk()
        self.create_canvas()

        self.ball = self.canvas.create_oval(
            180, 10, 190, 20, fill="grey"
        )

        self.vx = 3
        self.vy = 10

        self.width = 400
        self.height = 300

        self.create_pad()

        self.move_ball()

        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.focus_set()

        self.keys_pressed = set()
        self.move_pad()

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




    def create_pad(self):
        self.pad_width = 70
        self.pad_height = 10
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
        self.canvas.move(self.ball, self.vx, self.vy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= 400:
            self.vx *= -1

        if y1 <= 0 or y2 >= 300:
            self.vy *= -1

        self.root.after(30, self.move_ball)


    def key_press(self, event):
        self.keys_pressed.add(event.keysym.lower())


    def key_release(self, event):
        self.keys_pressed.discard(event.keysym.lower())


PlayingField()
