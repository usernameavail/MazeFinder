import pygame
from pygame.draw import rect, line
from pygame import display, Surface
import random
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKBLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

gradient = [
    (244, 1, 1),
    (235, 68, 3),
    (226, 96, 5),
    (216, 118, 6),
    (206, 136, 6),
    (196, 152, 7),
    (184, 167, 8),
    (173, 180, 9),
    (160, 193, 9),
    (146, 204, 10),
    (130, 216, 10),
    (113, 226, 11),
    (92, 236, 11),
    (65, 246, 12),
    (0, 255, 12),
]


class Maze(object):
    def __init__(self, window, c_width, dim, maze_width, maze_height):
        self.window = window
        self.c_width = c_width
        self.dim = dim
        self.maze_width = maze_width
        self.maze_height = maze_height

        self.solved = False

        self.yellow_cells = []
        self.grid_lines = []

        self.cell_stack = []
        self.grid = []
        self.path = {}
        self.my_path = []

    def knock(self, direction, x, y):
        if direction == "Up":
            coords = (
                (
                    x + 1,
                    y - self.c_width + 1,
                    self.c_width - 1,
                    2 * self.c_width - 1,
                ),
            )
        elif direction == "Down":
            coords = (
                (
                    x + 1,
                    y + 1,
                    self.c_width - 1,
                    2 * self.c_width - 1,
                ),
            )
        elif direction == "Left":
            coords = (
                (
                    x - self.c_width + 1,
                    y + 1,
                    2 * self.c_width - 1,
                    self.c_width - 1,
                ),
            )
        elif direction == "Right":
            coords = (
                (
                    x + 1,
                    y + 1,
                    2 * self.c_width - 1,
                    self.c_width - 1,
                ),
            )
        rect(
            self.window,
            YELLOW,
            coords,
            0,
        )
        self.yellow_cells.append(coords)

    def single_cell(self, x, y):
        rect(self.window, DARKBLUE, (x + 1, y + 1, self.c_width - 2, self.c_width - 2), 0)
        display.update()

    def recursive_cell(self, x, y):
        rect(self.window, YELLOW, (x + 1, y + 1, self.c_width - 2, self.c_width - 2), 0)
        display.update()

    def draw_maze(self):
        for crds in self.yellow_cells:
            rect(self.window, YELLOW, crds, 0)

    def make_maze(self):
        visited = []

        self.single_cell(self.maze_width, self.maze_height)
        self.cell_stack.append((self.maze_width, self.maze_height))
        visited.append((self.maze_width, self.maze_height))

        x = self.maze_width
        y = self.maze_height

        if self.grid == []:
            self.draw_grid()

        while len(self.cell_stack) > 0:
            time.sleep(0.01)
            cell = []

            if (x + self.c_width, y) not in visited and (x + self.c_width, y) in self.grid:
                cell.append("Right")
            if (x - self.c_width, y) not in visited and (x - self.c_width, y) in self.grid:
                cell.append("Left")
            if (x, y + self.c_width) not in visited and (x, y + self.c_width) in self.grid:
                cell.append("Down")
            if (x, y - self.c_width) not in visited and (x, y - self.c_width) in self.grid:
                cell.append("Up")

            if len(cell) > 0:
                current_cell = random.choice(cell)

                if current_cell == "Right":
                    self.knock("Right", x, y)
                    self.path[(x + self.c_width, y)] = x, y
                    x = x + self.c_width
                    self.cell_stack.append((x, y))
                    visited.append((x, y))

                elif current_cell == "Left":
                    self.knock("Left", x, y)
                    self.path[(x - self.c_width, y)] = x, y
                    x = x - self.c_width
                    self.cell_stack.append((x, y))
                    visited.append((x, y))

                elif current_cell == "Up":
                    self.knock("Up", x, y)  # lol
                    self.path[(x, y - self.c_width)] = x, y
                    y = y - self.c_width
                    self.cell_stack.append((x, y))
                    visited.append((x, y))

                elif current_cell == "Down":
                    self.knock("Down", x, y)
                    self.path[(x, y + self.c_width)] = x, y
                    y = y + self.c_width
                    self.cell_stack.append((x, y))
                    visited.append((x, y))

            else:
                x, y = self.cell_stack.pop()
                self.single_cell(x, y)
                time.sleep(0.05)
                self.recursive_cell(x, y)

    def draw_grid(self):
        y = 0
        for i in range(self.dim):
            x = self.c_width
            y += self.c_width
            for j in range(self.dim):
                line(self.window, BLACK, [x, y], [x + self.c_width, y], 2)  # Top Wall
                line(
                    self.window,
                    BLACK,
                    [x + self.c_width, y],
                    [x + self.c_width, y + self.c_width],
                    2,
                )  # Right Wall
                line(self.window, BLACK, [x, y], [x, y + self.c_width], 2)  # Left Wall
                line(
                    self.window,
                    BLACK,
                    [x, y + self.c_width],
                    [x + self.c_width, y + self.c_width],
                    2,
                )  # Bottom Wall

                self.grid.append((x, y))
                x += self.c_width

    # Work in progress
    def path_tracker(self, x, y):
        rect(self.window, GREEN, (x + 8, y + 8, 10, 10), 0)
        pygame.display.update()

    # Work in progress
    def solve(self):
        self.solution = []
        for i, val in enumerate(self.path.values()):
            if val == (self.c_width, self.c_width):
                break
            self.draw_grid()
            self.draw_maze()
            if i > 0:
                self.draw_solution()
            rect(
                self.window,
                gradient[i % len(gradient)],
                (val[0] + self.c_width / 2, val[1] + self.c_width / 2, 5, 5),
                0,
            )
            self.solution.append(val)
            display.update()
            print(val)
            print()
            time.sleep(0.2)
        self.solved = True

    def draw_solution(self):
        for i, val in enumerate(self.solution):
            rect(
                self.window,
                gradient[i % len(gradient)],
                (val[0] + self.c_width / 2, val[1] + self.c_width / 2, 5, 5),
                0,
            )
        # self.path_tracker(self.maze_width, self.maze_height)
        #
        # (x, y) = list(self.path.values())[0]
        # while (x, y) != (self.dim, self.dim):
        #     x, y = self.path[x, y]
        #     self.path_tracker(x, y)
        #     time.sleep(0.1)
