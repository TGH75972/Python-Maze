import tkinter as tk
import random

class MazeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Maze Game")
        self.master.geometry("600x600")
        
        self.grid_size = 10
        self.cell_size = 600 // self.grid_size
        self.current_level = 1
        self.max_levels = 3
        self.maze = []
        self.player_pos = [0, 0]
        self.goal_pos = [0, 0]
        self.create_maze()
        self.create_widgets()
        self.update_grid()
        
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
        self.canvas.pack()
        self.master.bind("<KeyPress>", self.on_key_press)
        self.draw_maze()
        self.draw_goal()
        self.display_level_info()

    def create_maze(self):
        self.maze = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player_pos = [0, 0]
        self.goal_pos = [self.grid_size - 1, self.grid_size - 1]
        self.add_walls()
        self.ensure_no_wall_at_start_goal()
        if self.current_level == 3:
            self.ensure_solvable_maze()

    def add_walls(self):
        wall_density = 0.1 + (self.current_level - 1) * 0.1
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if random.random() < wall_density and not (i == 0 and j == 0) and not (i == self.grid_size - 1 and j == self.grid_size - 1):
                    self.maze[i][j] = 1

    def ensure_no_wall_at_start_goal(self):
        """ Make sure the start and goal positions are clear of walls """
        self.maze[self.player_pos[0]][self.player_pos[1]] = 0
        self.maze[self.goal_pos[0]][self.goal_pos[1]] = 0

    def ensure_solvable_maze(self):
        """ Make sure there's a path from start to goal """
        if not self.is_solvable():
            self.create_maze()  # Recreate maze if not solvable

    def is_solvable(self):
        """ Check if there is a path from start to goal using DFS """
        visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        return self.dfs(self.player_pos[0], self.player_pos[1], visited)
    
    def dfs(self, x, y, visited):
        if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size or visited[x][y] or self.maze[x][y] == 1:
            return False
        if [x, y] == self.goal_pos:
            return True
        visited[x][y] = True
        return (self.dfs(x + 1, y, visited) or
                self.dfs(x - 1, y, visited) or
                self.dfs(x, y + 1, visited) or
                self.dfs(x, y - 1, visited))
        
    def draw_maze(self):
        self.canvas.delete("maze")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black" if self.maze[i][j] == 1 else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", tags="maze")

    def draw_player(self):
        self.canvas.delete("player")
        x1 = self.player_pos[1] * self.cell_size
        y1 = self.player_pos[0] * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline="blue", tags="player")

    def draw_goal(self):
        self.canvas.delete("goal")
        x1 = self.goal_pos[1] * self.cell_size
        y1 = self.goal_pos[0] * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="green", tags="goal")
        
    def update_grid(self):
        self.draw_maze()
        self.draw_player()
        self.draw_goal()
        self.display_level_info()
        
    def on_key_press(self, event):
        if event.keysym == "w":
            self.move_player(-1, 0)
        elif event.keysym == "s":
            self.move_player(1, 0)
        elif event.keysym == "a":
            self.move_player(0, -1)
        elif event.keysym == "d":
            self.move_player(0, 1)
        if self.player_pos == self.goal_pos:
            if self.current_level < self.max_levels:
                self.current_level += 1
                self.grid_size = 10 + self.current_level * 5
                self.cell_size = 600 // self.grid_size
                self.create_maze()
                self.update_grid()
            else:
                self.show_victory_message()
        
    def move_player(self, row_delta, col_delta):
        new_row = self.player_pos[0] + row_delta
        new_col = self.player_pos[1] + col_delta
        if 0 <= new_row < self.grid_size and 0 <= new_col < self.grid_size and self.maze[new_row][new_col] == 0:
            self.player_pos = [new_row, new_col]
            self.update_grid()
        
    def show_victory_message(self):
        self.canvas.create_text(self.grid_size * self.cell_size / 2, self.grid_size * self.cell_size / 2,
                                text="Congratulations! You completed all levels!", fill="red", font=("Arial", 24))

    def display_level_info(self):
        self.canvas.delete("info")
        info_text = f"Level: {self.current_level} / {self.max_levels}"
        self.canvas.create_text(self.grid_size * self.cell_size / 2, 20, text=info_text, fill="black", font=("Arial", 16), tags="info")

if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
