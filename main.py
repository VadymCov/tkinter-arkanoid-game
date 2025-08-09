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

