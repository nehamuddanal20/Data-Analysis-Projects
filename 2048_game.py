import tkinter as tk
import random
import os
import winsound  # Only works on Windows for sound

class Game2048:
    def __init__(self, master):
        self.master = master
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.tiles = []
        self.score = 0

        # Load high score from file
        try:
            with open("high_score.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0

        # Score display
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Helvetica", 16))
        self.score_label.grid(row=0, column=0, columnspan=4, pady=(10, 0))

        # High score display
        self.high_score_label = tk.Label(self.master, text=f"High Score: {self.high_score}", font=("Helvetica", 16))
        self.high_score_label.grid(row=1, column=0, columnspan=2)

        # Restart button
        self.restart_button = tk.Button(self.master, text="Restart", font=("Helvetica", 14), command=self.restart_game)
        self.restart_button.grid(row=1, column=2, columnspan=2)

        self.init_grid()
        self.add_tile()
        self.add_tile()
        self.update_grid()

        self.master.bind("<Key>", self.handle_key)

    def init_grid(self):
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                tile = tk.Label(self.master, text="", font=("Helvetica", 32), width=4, height=2, relief="raised")
                tile.grid(row=i + 2, column=j, padx=5, pady=5)  # Grid starts from row 2
                row.append(tile)
            self.tiles.append(row)

    def add_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                tile_color = self.get_tile_color(value)
                if value == 0:
                    self.tiles[i][j].configure(text="", bg=tile_color)
                else:
                    self.tiles[i][j].configure(text=str(value), bg=tile_color)
        self.master.update_idletasks()

    def handle_key(self, event):
        if event.keysym in ['Up', 'Down', 'Left', 'Right']:
            if self.move_tiles(event.keysym):
                self.add_tile()
                self.update_grid()
                if self.check_game_over():
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.high_score_label.config(text=f"High Score: {self.high_score}")
                        with open("high_score.txt", "w") as f:
                            f.write(str(self.high_score))
                    self.score_label.config(text=f"Game Over! Final Score: {self.score}")

    def move_tiles(self, direction):
        moved = False

        def move_row_left(row):
            new_row = [i for i in row if i != 0]
            for i in range(len(new_row) - 1):
                if new_row[i] == new_row[i + 1]:
                    new_row[i] *= 2
                    self.score += new_row[i]
                    self.score_label.config(text=f"Score: {self.score}")
                    winsound.Beep(500, 100)  # Beep on merge (Windows only)
                    new_row[i + 1] = 0
            new_row = [i for i in new_row if i != 0]
            return new_row + [0] * (self.grid_size - len(new_row))

        old_grid = [row[:] for row in self.grid]

        for i in range(self.grid_size):
            if direction == 'Left':
                self.grid[i] = move_row_left(self.grid[i])
            elif direction == 'Right':
                self.grid[i] = move_row_left(self.grid[i][::-1])[::-1]
            elif direction == 'Up':
                col = move_row_left([self.grid[j][i] for j in range(self.grid_size)])
                for j in range(self.grid_size):
                    self.grid[j][i] = col[j]
            elif direction == 'Down':
                col = move_row_left([self.grid[j][i] for j in range(self.grid_size)][::-1])[::-1]
                for j in range(self.grid_size):
                    self.grid[j][i] = col[j]

        if self.grid != old_grid:
            moved = True
        return moved

    def check_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def restart_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.add_tile()
        self.add_tile()
        self.update_grid()

    def get_tile_color(self, value):
        colors = {
            0: "lightgray",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32"
        }
        return colors.get(value, "#3c3a32")  # fallback color for large tiles


if __name__ == "__main__":
    root = tk.Tk()
    root.title("2048 Game")
    game = Game2048(root)
    root.mainloop()
