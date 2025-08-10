import tkinter as tk
import random

class ArkanoidGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ArkanoidGame")
        self.create_canvas()

        self.width = 452
        self.height = 350
        self.root.resizable(False, False)

        self.game_running = False
        self.life = 3
        self.score = 0
        self.lvl = 1
        self.row = -1

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
        self.canvas = tk.Canvas(self.root, width=452, height=350, bg="gray4")
        self.canvas.pack()

    def create_bricks(self):
        self.bricks = []
        bricks_weidth = 53
        bricks_height = 10
        bricks_padding = 2
        self.row += 1

        for row in range(self.row):
            for col in range(8):
                x1 = col * (bricks_weidth + bricks_padding) + bricks_padding + 5
                y1 = row * (bricks_height + bricks_padding) + 20
                x2 = x1 + bricks_weidth
                y2 = y1 + bricks_height

                brick = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    tags = "bricks",
                    fill = "tan",
                    outline = "indianred3"
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

    def create_ball(self):
        self.ball_radius = 4
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2 + 50
        self.ball_dx = random.choice([-3,3]) # speed
        self.ball_dy = - 3 # speed

        self.ball = self.canvas.create_oval(
            self.ball_x - self.ball_radius,
            self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius,
            self.ball_y + self.ball_radius,
            fill = "gold1",
            outline = "gray10",
            tags = "ball"
        )

    def key_press(self, event):
        self.keys_pressed.add(event.keysym.lower())

        if event.keysym == "space" and not self.game_running and self.life == 3:
            self.restart_game()

        if not self.game_running:
            return

        self.keys_pressed.add(event.keysym.lower())

    def key_release(self, event):
        if not self.game_running:
            return
        self.keys_pressed.discard(event.keysym.lower())

    def move_pad(self):
        if "a" in self.keys_pressed:
            if self.pad_x >= 0:
                self.pad_x -= self.pad_speed

        if "d" in self.keys_pressed:
            if self.pad_x <= self.width - self.pad_width:
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
                self.ball_x + self.ball_radius >= self.pad_x and
                self.ball_x - self.ball_radius <= self.pad_x + self.pad_width and
                self.ball_y + self.ball_radius >= self.pad_y and
                self.ball_y - self.ball_radius <= self.pad_y + self.pad_height
        ):
            # platform bounce physics
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
                    self.ball_x + self.ball_radius >= x1 and
                    self.ball_x - self.ball_radius <= x2 and
                    self.ball_y + self.ball_radius >= y1 and
                    self.ball_y - self.ball_radius <= y2
            ):

                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.canvas.update()
                self.score += 10
                self.ball_dy += -0.5
                self.pad_speed += 0.3

                # Bounce
                self.ball_dy = -self.ball_dy
                break

        if self.ball_y + self.ball_radius > self.height:
            self.life -= 1
            self.canvas.delete("ball")
            self.create_ball()

        if self.life == 0:
            self.game_over()

        self.test_for_victory()

        self.canvas.coords(
            self.ball,
            self.ball_x - self.ball_radius,
            self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius,
            self.ball_y + self.ball_radius
        )

    def test_for_victory(self):
        if not self.bricks:
            self.canvas.create_text(
                225,
                100,
                text= "VICTORY",
                fill= "darksalmon"
            )
            self.game_running = False
            self.lvl += 1
            self.countdown_to_restart(5)

    def update_ui(self):
        self.canvas.itemconfig(
            self.score_text, text= f"Score: {self.score}"
        )
        self.canvas.itemconfig(
            self.life_text, text= f"Life: {self.life}"
        )
        self.canvas.itemconfig(
            self.lvl_text, text= f"Lvl: {self.lvl}"
        )

    def display_interface(self):
        self.lvl_text = self.canvas.create_text(
            self.width // 2,
            10,
            text= f"Lvl: {self.lvl}",
            fill= "darksalmon"
        )
        self.score_text = self.canvas.create_text(
            50, 10,
            text= f"Score: {self.score}",
            fill= "darksalmon"
        )
        self.life_text = self.canvas.create_text(
            400, 10,
            text= f"Life: {self.life}",
            fill= "darksalmon"
        )
        self.start_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text= f"      ⏪a...srart space...b⏩\n",
            font= ("Arial", 12),
            fill= "darksalmon"
        )

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(
            225, 100,
            text = "Game Over ",
            fill="darksalmon"
        )
        self.countdown_to_restart(5)

    def countdown_to_restart(self, seconds):

        if hasattr(self, "restart_text"):
            self.canvas.delete(self.restart_text)

        self.restart_text = self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Restart game via {seconds}",
            fill="darksalmon"
        )

        if seconds > 0:
            self.root.after(1000, self.countdown_to_restart, seconds - 1)
        else:
            self.restart_game()

    def restart_game(self):
        self.canvas.delete("all")
        self.keys_pressed.clear()

        self.game_running = True
        self.life = 3
        self.score = 0

        self.display_interface()
        self.canvas.delete(self.start_text)

        self.create_bricks()
        self.create_ball()
        self.create_pad()

        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)

        self.game_loop()

    def game_loop(self):
        if self.game_running:
            self.move_ball()
            self.move_pad()
            self.update_ui()
            self.root.after(30, self.game_loop)

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    start_game = ArkanoidGame()
    start_game.run()
